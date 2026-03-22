import logging
from dotenv import load_dotenv
load_dotenv()
import os
from agents.prompts import RETRIEVAL_AGENT_SYSTEM_PROMPT
from uuid import UUID
from redis.asyncio import Redis
import json
from config import config

logger = logging.getLogger(__name__)


redis_client = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=os.getenv("REDIS_PORT", 6379),
    decode_responses=True
)


async def gemini_chat(chat_id: UUID, user_query: str):
    logger.debug("Gemini chat...")
    from agents.clients import gemini_client
    # Need to integrate manual chat session management for gemini
    # global chat_history

    response = await gemini_client.invoke_gemini(
        user_query=user_query
    )
    
    return response


async def ollama_chat(chat_id: UUID, user_query: str):
    logger.debug("Ollama chat...")
    from agents.clients import ollama_client

    chat_history_redis = await redis_client.get(name=str(chat_id))
    chat_history = json.loads(chat_history_redis) if chat_history_redis else []

    response, new_messages = await ollama_client.invoke_ollama(
        user_query=user_query,
        system_prompt=RETRIEVAL_AGENT_SYSTEM_PROMPT,
        chat_history=chat_history
    )
    chat_history.extend(new_messages)

    await redis_client.set(
        name=str(chat_id),
        value=json.dumps(chat_history),
        ex=config.CHAT_SESSION_TTL
    )
    
    return response