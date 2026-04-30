from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth_routes import app as auth_router
from pydantic import BaseModel
from crypto import encrypt, decrypt
import base64

class Item(BaseModel):
    text: str

app = FastAPI(title="API de cifrado", 
              description="Una API para cifrar y descifrar texto y archivos", 
              version="2.0.0")

app.include_router(auth_router, prefix="/auth", tags=["auth"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Recibida solicitud: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Respuesta enviada: {response.status_code}")
    return response

@app.on_event("startup")
async def startup_event():
    print("La API de cifrado ha iniciado correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    print("La API de cifrado se está cerrando")

@app.get("/")
async def root():
    return {"message": "API de cifrado correcto"}

@app.get("/items")
async def get_items():
    return [{"text": "Item 1"}, {"text": "Item 2"}]

connected_clients = []
async def websocket_message(websocket: WebSocket, message: str):
        await websocket.accept()
        connected_clients.append(websocket)
        try:
            while True:
                message = await websocket.receive_text()
                await websocket_message(websocket, message)
        except:
            connected_clients.remove(websocket)

@app.post("/encrypt")
async def encrypt_route(item: Item):
    cipher_text = encrypt(item.text)
    return {"cipher": cipher_text}

@app.post("/decrypt")
async def decrypt_route(data: dict):
    if "cipher" not in data:
        raise HTTPException(status_code=400, 
                            detail="Falta el campo 'cipher' en la solicitud")

    plain_text = decrypt(data["cipher"])
    return {"text": plain_text}

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