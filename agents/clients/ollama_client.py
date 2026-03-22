from dotenv import load_dotenv
load_dotenv()
import logging
from ollama import AsyncClient
import os

from agents.tools.retrieval_tools import sql_tool, policy_query_tool

logger = logging.getLogger(__name__)

ollama_async_client = AsyncClient(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.getenv("OLLAMA_API_KEY")}
)

available_tools = {
    "sql_tool": sql_tool,
    "policy_query_tool": policy_query_tool
}

async def invoke_ollama(
        user_query: str,
        system_prompt: str | None,
        chat_history: list = []
):
    logger.debug("Invoking Ollama...")

    compiled_chat = []
    if system_prompt:
        compiled_chat.append({"role": "system", "content": system_prompt})
    compiled_chat.extend(chat_history)
    compiled_chat.append({"role": "user", "content": user_query})
    
    new_messages = [{"role": "user", "content": user_query}]

    # Tool loop
    while(True):

        response = await ollama_async_client.chat(
            model="gpt-oss:120b",
            messages=compiled_chat,
            tools=[
                sql_tool,
                policy_query_tool
            ],
            think=False
        )
        compiled_chat.append(response.message)
        new_messages.append(response.message)

        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                if tool_call.function.name in available_tools:
                    logger.debug(f"Calling {tool_call.function.name} with arguments {tool_call.function.arguments}")
                    result = available_tools[tool_call.function.name](**tool_call.function.arguments)
                    logger.debug(f"Result : {result}")
                    compiled_chat.append({"role": "tool", "tool_name": tool_call.function.name, "content": str(result)})
                    new_messages.append({"role": "tool", "tool_name": tool_call.function.name, "content": str(result)})
        else:
            break
    
    return response.message.content, new_messages
