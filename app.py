from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return 'Assistente do vereador está rodando corretamente!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    print("📦 Dados recebidos:", data)

    mensagem = data.get("message")
    telefone = data.get("sender", {}).get("id")

    if not mensagem or not telefone:
        return jsonify({"erro": "Mensagem ou telefone ausente"}), 400

    resposta = f"Recebemos sua mensagem: {mensagem}"

    zapi_url = f"https://api.z-api.io/instances/{os.getenv('ZAPI_INSTANCE_ID')}/token/{os.getenv('ZAPI_TOKEN')}/send-message"

    payload = {
        "phone": telefone,
        "message": resposta
    }

    requests.post(zapi_url, json=payload)

    return jsonify({"status": "mensagem enviada", "resposta": resposta})
