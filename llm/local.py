"""
Interface for interacting with a locally hosted Ollama language model.

This module provides helper functions for sending prompts to an
Ollama server and receiving generated responses. It acts as the
single communication layer between the application and the language
model, allowing the rest of the project to remain independent of
HTTP requests and Ollama-specific API details.
"""

import requests

from config import (
    OLLAMA_MODEL,
    OLLAMA_URL,
)


def generate(
    prompt: str,
    temperature: float = 0.0,
    num_predict: int = 256,
    think: bool = False,
) -> str:
    """
    Generate text using the local Ollama model.

    Args:
        prompt:
            Prompt sent to the language model.

        temperature:
            Sampling temperature controlling response randomness.

        num_predict:
            Maximum number of tokens to generate.

        think:
            Enables reasoning output for models that support it.

    Returns:
        str:
            Generated response from the language model.

    Raises:
        requests.HTTPError:
            Raised if the Ollama API returns an unsuccessful
            HTTP status code.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "think": think,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
        },
    }

    # Send the generation request to Ollama.
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=600,
    )

    response.raise_for_status()

    data = response.json()

    _print_debug_information(data)

    return data.get("response", "")


def _print_debug_information(data: dict) -> None:
    """
    Print diagnostic information returned by the Ollama API.

    This helper is intended for development and debugging.
    It displays generation statistics such as token counts,
    completion status and optional reasoning output.

    Args:
        data:
            JSON response returned by the Ollama API.
    """

    print("\n================ OLLAMA ================\n")

    print("Model:", data.get("model"))
    print("Done:", data.get("done"))
    print("Done reason:", data.get("done_reason"))
    print("Prompt tokens:", data.get("prompt_eval_count"))
    print("Generated tokens:", data.get("eval_count"))

    thinking = data.get("thinking", "")

    if thinking:

        print("\nThinking:\n")
        print(thinking[:500])

    print("\n========================================\n")
