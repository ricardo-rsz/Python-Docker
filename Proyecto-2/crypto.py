from config import SECRET_KEY
from cryptography.fernet import Fernet

cipher = Fernet(SECRET_KEY)

def encrypt(text: str) -> str:
    encrypt = cipher.encrypt(text.encode())
    return encrypt.decode()

def decrypt(cipher_text: str) -> str:
    decrypt = cipher.decrypt(cipher_text.encode())
    return decrypt.decode()