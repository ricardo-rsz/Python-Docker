from flask import Flask, jsonify, request
from crypto import encrypt, decrypt
import base64

app = Flask(__name__)

@app.route("/")
def root():
    return "API de cifrado correcto"

@app.route("/encrypt", methods=["POST"])
def encrypt_route():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Falta el campo 'text'"}), 400
    
    text = data["text"]
    cipher = encrypt(text)

    return jsonify({"cipher": cipher})

@app.route("/decrypt", methods=["POST"])
def decrypt_route():
    data = request.get_json()

    if not data or "cipher" not in data:
        return jsonify({"error": "Falta el campo 'cipher'"}), 400
    
    cipher_text = data["cipher"]
    text = decrypt(cipher_text)

    return jsonify({"text": text})

@app.route("/encrypt-file", methods=["POST"])
def encrypt_file_route():
    if "file" not in request.files:
        return jsonify({"error": "Falta el archivo"}), 400
    
    file = request.files["file"]
    content = file.read()

    try:
        text_content = content.decode("utf-8")
    except UnicodeDecodeError:
        text_content = base64.b64encode(content).decode("utf-8") 

    cipher = encrypt(text_content)
    return jsonify({"filename": file.filename, "cipher": cipher})

if __name__=="__main__":
    app.run(debug=True)