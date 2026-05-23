import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generar_analisis(datos):

    prompt = f"""
    Analiza los siguientes datos del sistema ServiTech Manager
    y genera una conclusión profesional y recomendaciones:

    {datos}
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek/deepseek-chat:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    resultado = response.json()

    print(resultado)

    if "choices" in resultado:
        return resultado["choices"][0]["message"]["content"]

    return "No se pudo generar el análisis inteligente."