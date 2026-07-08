import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"  # Local web server address, 11434 is default Ollama port, /api/generate is endpoint that generates text
OLLAMA_MODEL = "qwen2.5:3b"
