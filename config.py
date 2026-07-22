# Third-party import
from dotenv import load_dotenv

# ------------------------------------
# Load the application configuration.
# ------------------------------------

# Load environment variables
load_dotenv()

# Ollama API configuration
OLLAMA_URL = "http://localhost:11434/api/generate"

# Ollama model
OLLAMA_MODEL = "qwen3:8b"
