import logging
from agents.prompts import RETRIEVAL_AGENT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


chat_history = []


async def gemini_chat(user_query: str):
    logger.debug("Gemini chat...")
    from agents.clients import gemini_client
    # Need to integrate manual chat session management for gemini
    # global chat_history

    response = await gemini_client.invoke_gemini(
        user_query=user_query
    )
    
    return response


async def ollama_chat(user_query: str):
    logger.debug("Ollama chat...")
    from agents.clients import ollama_client
    global chat_history

    response, new_messages = await ollama_client.invoke_ollama(
        user_query=user_query,
        system_prompt=RETRIEVAL_AGENT_SYSTEM_PROMPT,
        chat_history=chat_history
    )
    chat_history.extend(new_messages)
    
    return response