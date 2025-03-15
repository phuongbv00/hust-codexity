import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

class Settings:
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8083))

settings = Settings()