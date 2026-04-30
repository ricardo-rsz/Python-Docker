import os
from dotenv import load_dotenv
from pathlib import Path


#Definir la ruta del archivo .env
env_path = Path("./.env")

#Comprobar que el archivo existe
if not env_path.exists():
    raise FileNotFoundError(f"No se encontró el archivo .env en: {env_path}")



#Cargar las variables del archivo .env
load_dotenv(dotenv_path=env_path)



#Leer la variable SECRET_KEY
SECRET_KEY = os.getenv("SECRET_KEY").encode()

#Comprobar de que SECRET_KEY exista
if not SECRET_KEY:
    raise ValueError("SECRET_KEY no está definida en el archivo .env")