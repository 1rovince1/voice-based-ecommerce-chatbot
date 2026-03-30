import os

from dotenv import load_dotenv
load_dotenv()


OLLAMA_API_KEY=os.getenv("OLLAMA_API_KEY")

REDIS_HOST=os.getenv("REDIS_HOST")
REDIS_PORT=os.getenv("REDIS_PORT")

CHAT_SERVICE_API_AUTH_KEY=os.getenv("CHAT_SERVICE_API_AUTH_KEY")