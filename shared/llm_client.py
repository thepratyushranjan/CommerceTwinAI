from google import genai
from google.genai import types
from shared.config import config

def get_client() -> genai.Client:
    """Returns a configured Gemini client with an extended timeout to prevent 503 errors."""
    config.validate()
    # Setting timeout to 120 seconds (120,000ms) to handle complex vision tasks
    return genai.Client(
        api_key=config.GOOGLE_API_KEY,
        http_options=types.HttpOptions(timeout=120_000)
    )
