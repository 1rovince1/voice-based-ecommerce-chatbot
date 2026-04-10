from utils.logger_config import setup_logging
setup_logging()
import logging

from agents.rag_agent.agent import ollama_rag_agent
from agents.stt_agent.agent import stt_agent

logger = logging.getLogger(__name__)


from uuid import uuid4
application_context = {
    "session_id": uuid4()
}

async def execute_workflow():
    while(True):
        logger.info("Executing agentic workflow...")
        recorded_text = await stt_agent()
        agent_response = await ollama_rag_agent(
            user_query=recorded_text,
            application_context=application_context
        )
        logger.info(f"Response: {agent_response}")

import asyncio
asyncio.run(execute_workflow())
