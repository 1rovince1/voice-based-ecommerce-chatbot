import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Header

from api.schemas.chat import ChatRequest
from agents.chat_agent.agent import ollama_chat_agent


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/agent/v1/chat")
async def chat_request(
    request: ChatRequest,
    session_id: Annotated[UUID, Header()]
):
    
    try:
        application_context = {
            "session_id": session_id
        }
        chat_agent_response = await ollama_chat_agent(
            user_query=request.user_query,
            application_context=application_context
        )

        return {
            "chat_agent_response": chat_agent_response,
            "session_id": session_id
        }
        
    except Exception as e:
        logger.exception(f"Error in API request routing: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(f"Error in API request routing: {str(e)}")
        )