import logging
from google.genai import Client, types
from dotenv import load_dotenv
import os
load_dotenv()

from agents.tools.retrieval_tools import sql_tool, policy_query_tool
from agents.prompts import RETRIEVAL_AGENT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


gemini_client = Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = RETRIEVAL_AGENT_SYSTEM_PROMPT

gemini_config_with_tools = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,
    thinking_config=types.ThinkingConfig(thinking_budget=0),
    tools=[sql_tool, policy_query_tool]
)

chat_session = gemini_client.aio.chats.create(
    model="gemini-2.5-flash",
    config=gemini_config_with_tools
)


async def invoke_gemini(user_query: str):
    logger.debug("Invoking Gemini...")
    response = await chat_session.send_message(message=user_query)
    return response.text
