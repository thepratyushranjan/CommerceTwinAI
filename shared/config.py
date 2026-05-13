import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    @classmethod
    def validate(cls):
        if not cls.GOOGLE_API_KEY or cls.GOOGLE_API_KEY == "your_gemini_api_key_here":
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in .env file.")

config = Config()
