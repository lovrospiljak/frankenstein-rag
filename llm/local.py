import requests  # HTTP requests

from config import OLLAMA_MODEL, OLLAMA_URL


# This file only talks to the LLM
# Sends a prompt to the local Ollama model
def generate_answer(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,  # Sends the whole answer instead of word by word
        "options": {
            "temperature": 0.2,
            "num_predict": 150,
        },
    }

    # Sending the request
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()  # Error check

    return response.json()["response"]
