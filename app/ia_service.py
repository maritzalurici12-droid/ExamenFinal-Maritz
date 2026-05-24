import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generar_analisis(datos):

    prompt = f"""
    Analiza los siguientes datos del sistema ServiTech Manager
    y genera una conclusión profesional y breve:

    {datos}
    """

    try:

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "http://localhost:8080",
                "X-Title": "ServiTech Manager",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-3.5-turbo",
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

        return "La IA no pudo generar el análisis."

    except Exception as e:
        return f"Error IA: {str(e)}"