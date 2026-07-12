# Third-party imports
import requests

# Local imports
from config import OLLAMA_MODEL, OLLAMA_URL

# ---------------------------------------
# Generate response using the local LLM.
# ---------------------------------------


def generate_answer(prompt):
    """Generate an answer using the local Ollama model."""

    # Build the request payload
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,  # Send the whole answer instead of word by word
        "options": {
            "temperature": 0.2,
            "num_predict": 150,
        },
    }

    # Send the request to Ollama
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )

    # Raise an exception if the request failed
    response.raise_for_status()

    # Parse the response
    data = response.json()

    # Return the generated response
    return data["response"]
