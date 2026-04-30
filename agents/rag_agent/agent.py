import logging
import json

from services.llm.ollama_llm import invoke_ollama_llm
from agents.rag_agent.prompts import CHAT_AGENT_SYSTEM_PROMPT
from agent_tools.adapter import build_ollama_tools
from agent_tools.registry.retrieval import TOOLS as RETRIEVAL_TOOLS
from clients.redis_client import redis_manager
from config import settings


logger = logging.getLogger(__name__)


MAX_CHAT_SESSION_MESSAGES = settings.MAX_CHAT_SESSION_MESSAGES

tool_registry = RETRIEVAL_TOOLS
ollama_tools = build_ollama_tools(tool_registry)


async def ollama_rag_agent(
        user_query: str,
        application_context: dict
) -> str:
    
    logger.debug("Ollama chat...")

    chat_history_redis = await redis_manager.client.get(name=str(application_context["session_id"]))
    chat_history = json.loads(chat_history_redis) if chat_history_redis else []

    response, new_messages = await invoke_ollama_llm(
        user_query=user_query,
        system_prompt=CHAT_AGENT_SYSTEM_PROMPT,
        chat_history=chat_history,
        available_tools=ollama_tools,
        tool_registry=tool_registry,
        application_context=application_context
    )
    chat_history.extend(new_messages)
    chat_to_save = chat_history[-MAX_CHAT_SESSION_MESSAGES:]

    # remove initial messages in trimmed chat if it was not user or assistant message
    while chat_to_save and chat_to_save[0]["role"] == "tool":
        chat_to_save.pop(0)
    # remove last message if it is unresponded tool call by LLM
    while chat_to_save and chat_to_save[-1]["role"] == "assistant" and chat_to_save[-1].get("tool_calls"):
        chat_to_save.pop()

    await redis_manager.client.set(
        name=str(application_context["session_id"]),
        value=json.dumps(chat_to_save),
        ex=settings.CHAT_SESSION_TTL
    )
    
    return response