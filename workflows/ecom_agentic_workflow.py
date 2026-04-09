import logging

from agents.rag_agent.agent import ollama_rag_agent
from agents.stt_agent.agent import stt_agent

logger = logging.getLogger(__name__)


while(True):
    recorded_text = await stt_agent()
    agent_response = await ollama_rag_agent(
        user_query=recorded_text
        application_context=application_context
    )
    logger.info(f"Response: {agent_response}")
