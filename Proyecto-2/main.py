
from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth_routes import router as auth_router
from pydantic import BaseModel
from crypto import encrypt, decrypt
import base64

# Pydantic models

class Item(BaseModel):
    text: str

class CipherRequest(BaseModel):
    cipher: str

class EncryptResponse(BaseModel):
    cipher: str

class DecryptResponse(BaseModel):
    text: str

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

@app.get("/")
async def root():
    return {"message": "API de cifrado correcto"}

@app.get("/items")
async def get_items():
    return [{"text": "Item 1"}, {"text": "Item 2"}]

connected_clients = []

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

@app.post("/encrypt")
async def encrypt_route(item: Item):
    cipher_text = encrypt(item.text)
    return {"cipher": cipher_text}

@app.post("/decrypt")
async def decrypt_route(request: CipherRequest):
    try:
        decrypted_text = decrypt(request.cipher)
        return {"text": decrypted_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/encrypt-file")
async def encrypt_file_route(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Falta el archivo en la solicitud")

    content = await file.read()

    try:
        text_content = content.decode("utf-8")
    except UnicodeDecodeError:
        text_content = base64.b64encode(content).decode("utf-8") 

    cipher_text = encrypt(text_content)
    return {"filename": file.filename, "cipher": cipher_text}