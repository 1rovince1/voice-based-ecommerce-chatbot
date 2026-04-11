import os

from dotenv import load_dotenv
load_dotenv()


OLLAMA_API_KEY: str = os.getenv("OLLAMA_API_KEY")

REDIS_HOST: str = os.getenv("REDIS_HOST")
REDIS_PORT: str = os.getenv("REDIS_PORT")

CHAT_SERVICE_API_AUTH_KEY: str = os.getenv("CHAT_SERVICE_API_AUTH_KEY")

FASTAPI_BACKEND_URL: str = os.getenv("FASTAPI_BACKEND_URL")