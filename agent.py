from google.genai import Client, types
from dotenv import load_dotenv
import os
load_dotenv()

from retrieval import sql_tool
from prompts import RETRIEVAL_AGENT_SYSTEM_PROMPT

gemini = Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = RETRIEVAL_AGENT_SYSTEM_PROMPT

gemini_config_with_tools = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,
    thinking_config=types.ThinkingConfig(thinking_budget=0),
    tools=[sql_tool]
)

chat_session = gemini.aio.chats.create(
    model="gemini-2.5-flash",
    config=gemini_config_with_tools
)


async def send_async_message(user_query: str):
    response = chat_session.send_message(message=user_query)
    print(f"AI: {response.text}")
    return response.text