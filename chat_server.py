from dotenv import load_dotenv
load_dotenv()
from logger_config import setup_logging
setup_logging()
import logging
import os
import asyncio
from uuid import uuid4

logger = logging.getLogger(__name__)


def select_chat_provider():
    if os.getenv("GEMINI_API_KEY"):
        logger.info("Found Gemini key, starting Gemini based chat session...")
        from agents.chat_agent import gemini_chat
        return gemini_chat
    
    elif os.getenv("OLLAMA_API_KEY"):
        logger.info("Found Ollama api key, starting Ollama based chat session...")
        from agents.chat_agent import ollama_chat
        return ollama_chat
    
    raise RuntimeError("No LLM provider configured")


logger.debug("Starting main")
async def main():
    logger.debug("Starting chat")
    ai_chat = select_chat_provider()
    chat_id = uuid4()
    
    while(True):
        user_query = input("User: ")

        if user_query == "/exit":
            logger.info("Thank you!!")
            break

        ai_response = await ai_chat(
            chat_id=chat_id,
            user_query=user_query
        )
        logger.info(f"AI: {ai_response}\n")


asyncio.run(main())