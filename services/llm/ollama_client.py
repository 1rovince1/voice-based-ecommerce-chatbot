import logging
import json

from ollama import AsyncClient

from agent_tools.dispatcher import dispatch_tool
from config import settings, env_vars


logger = logging.getLogger(__name__)


ollama_async_client = AsyncClient(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + env_vars.OLLAMA_API_KEY}
)


async def invoke_ollama(
        user_query: str,
        system_prompt: str | None,
        chat_history: list | None = None,
        available_tools: list | None = None,
        tool_registry: dict | None = None,
        application_context: dict | None = None
) -> tuple[str, list]:
    
    logger.debug("Invoking Ollama...")
    chat_history = chat_history or []
    available_tools = available_tools or []
    tool_registry = tool_registry or {}

    compiled_chat = []
    if system_prompt:
        compiled_chat.append({"role": "system", "content": system_prompt})
    compiled_chat.extend(chat_history)
    
    new_messages = [{"role": "user", "content": user_query}]

    tool_loop_try = 1
    MAX_TOOL_LOOP_ITERATIONS = settings.MAX_TOOL_LOOP_ITERATIONS

    # Tool loop
    while(True):
        response = await ollama_async_client.chat(
            model=settings.OLLAMA_LLM_MODEL,
            messages=compiled_chat + new_messages,
            tools=available_tools,
            think=False
        )

        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                if tool_call.function.name in tool_registry:
                    new_messages.append({
                        "role": "assistant",
                        "content": response.message.content,
                        "tool_calls": [tool_call.model_dump()]
                    })

                    logger.info(f"Calling {tool_call.function.name} with arguments {tool_call.function.arguments}")
                    
                    tool_args = tool_call.function.arguments
                    if isinstance(tool_args, str):
                        tool_args = json.loads(tool_args)

                    try:
                        result = await dispatch_tool(
                            registry=tool_registry,
                            tool_name=tool_call.function.name,
                            args=tool_call.function.arguments,
                            application_context=application_context
                        )
                        logger.info(f"Result : {result}")

                        new_messages.append({
                            "role": "tool",
                            "tool_name": tool_call.function.name,
                            "content": str(result)
                        })
                    
                    except Exception as e:
                        new_messages.append({
                            "role": "tool",
                            "tool_name": tool_call.function.name,
                            "content": str(e)
                        })

        else:
            new_messages.append({
                "role": "assistant",
                "content": response.message.content
            })
            break

        # Iteration limit for agent
        tool_loop_try += 1
        if tool_loop_try > MAX_TOOL_LOOP_ITERATIONS:
            failure_msg = "Sorry, I am not able to find data for the given request."
            new_messages.append({
                "role": "assistant",
                "content": failure_msg
            })
            return failure_msg, new_messages
    
    return response.message.content, new_messages