
from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth_routes import router as auth_router
from typing import List
from pydantic import BaseModel
from pydantic import Field
from crypto import encrypt, decrypt
import base64

# Pydantic models

class Item(BaseModel):
    text: str = Field(..., description="El texto del ítem")

class CipherRequest(BaseModel):
    cipher: str = Field(..., description="El texto cifrado")
    
class EncryptResponse(BaseModel):
    cipher: str = Field(..., description="El texto cifrado")

class DecryptResponse(BaseModel):
    text: str = Field(..., description="El texto descifrado")

class MessageResponse(BaseModel):
    message: str = Field(..., description="El mensaje de respuesta")

class FileEncryptResponse(BaseModel):
    filename: str = Field(..., description="El nombre del archivo")
    cipher: str = Field(..., description="El texto cifrado")

# APP

app = FastAPI(title="API de cifrado", 
              description="Una API para cifrar y descifrar texto y archivos", 
              version="2.0.1")

app.include_router(auth_router, prefix="/auth", tags=["auth"])

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware y eventos

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Solicitud entrante: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Respuesta enviada: {response.status_code}")
    return response

@app.on_event("startup")
async def startup_event():
    print("La API de cifrado ha iniciado correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    print("La API de cifrado se está cerrando")

# Rutas

@app.get("/", response_model=MessageResponse)
async def root():
    return MessageResponse(message="Bienvenido a la API de cifrado")

@app.get("/items", response_model=List[Item])
async def get_items():
    return [Item(text="Item 1"), Item(text="Item 2"), Item(text="Item 3")]

connected_clients: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Mensaje recibido: {data}")
            for client in connected_clients:
                if client != websocket:
                    await client.send_text(f"Nuevo mensaje: {data}")
    except Exception as e:
        print(f"Error en WebSocket: {e}")
    finally:
        connected_clients.remove(websocket)
        print("Cliente desconectado")

@app.post("/encrypt", response_model=EncryptResponse)
async def encrypt_route(request: Item):
    try:
        cipher_text = encrypt(request.text)
        return EncryptResponse(cipher=cipher_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/decrypt", response_model=DecryptResponse)
async def decrypt_route(request: CipherRequest):
    try:
        decrypted_text = decrypt(request.cipher)
        return DecryptResponse(text=decrypted_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/encrypt-file", response_model=FileEncryptResponse)
async def encrypt_file_route(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Falta el archivo en la solicitud")

    content = await file.read()

    try:
        text_content = content.decode("utf-8")
    except UnicodeDecodeError:
        text_content = base64.b64encode(content).decode("utf-8") 

    cipher_text = encrypt(text_content)
    return FileEncryptResponse(filename=file.filename, cipher=cipher_text)