import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

async def gerar_resposta_huggingface(message):
    API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    prompt = f"{message}"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 120,
            "num_return_sequences": 1,
            "temperature": 0.7
        }
    }

    for _ in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            print(f"Status Code: {response.status_code}")
            print(f"Resposta Completa: {response.text}")

            if response.status_code == 200:
                return response.json()[0]['generated_text'].strip()
            elif response.status_code == 503:
                print("Modelo carregando. Tentando novamente...")
                time.sleep(5)
            else:
                return f"Erro ao gerar resposta: {response.status_code}"

        except Exception as e:
            print(f"Erro ao gerar resposta: {e}")
            return "Houve um erro ao tentar gerar a resposta."

    return "Desculpe, o modelo ainda está indisponível. Tente novamente mais tarde."