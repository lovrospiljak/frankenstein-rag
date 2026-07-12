# Standard library import
import os

# Third-party import
from dotenv import load_dotenv

# ------------------------------------
# Load the application configuration.
# ------------------------------------

# Load environment variables
load_dotenv()

# Ollama API configuration
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate",
)

# Ollama model
OLLAMA_MODEL = "qwen2.5:3b"
