import logging

from ollama import AsyncClient

from config import env_vars

logger = logging.getLogger(__name__)


class OllamaClient:
    def __init__(self):
        self.client = None


    async def connect(self):
        logger.info("Connecting Ollama client...")
        self.client = AsyncClient(
            host="https://ollama.com",
            headers={"Authorization": "Bearer " + env_vars.OLLAMA_API_KEY}
        )
        logger.info("Ollama client connected successfully.")


    async def disconnect(self):
        logger.info("Disconnecting Ollama client...")
        self.client = None
        logger.info("Ollama client disconnected successfully.")


ollama_manager = OllamaClient()