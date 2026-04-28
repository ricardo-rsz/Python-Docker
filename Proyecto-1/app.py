from flask import Flask, jsonify, request
from crypto import encrypt, decrypt

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

if __name__=="__main__":
    app.run(debug=True)