from config import SECRET_KEY
from cryptography.fernet import Fernet

cipher = Fernet(SECRET_KEY)

def encrypt(text):
    encrypt = cipher.encrypt(text.encode())
    return encrypt.decode()

def decrypt(cipher_text):
    decrypt = cipher.decrypt(cipher_text.encode())
    return decrypt.decode()