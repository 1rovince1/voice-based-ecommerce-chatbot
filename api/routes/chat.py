import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Header

from api.schemas.chat import ChatRequest, VoiceChatRequest
from agents.rag_agent.agent import ollama_rag_agent


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(path="/agent/v1/chat")
async def chat_request(
    request: ChatRequest,
    session_id: Annotated[UUID, Header()]
):
    try:
        application_context = {
            "session_id": session_id
        }
        chat_agent_response = await ollama_rag_agent(
            user_query=request.user_query,
            application_context=application_context
        )
        return {
            "chat_agent_response": chat_agent_response,
            "session_id": session_id
        }
        
    except Exception as e:
        logger.exception(f"Error in API request routing", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(f"Error in API request routing: {str(e)}")
        )


# @router.post(path="/agent/v1/voice_chat")
@router.get(path="/agent/v1/voice_chat")
async def voice_chat_request(
    # request: VoiceChatRequest,
    session_id: Annotated[UUID, Header()]
):
    try:
        import asyncio
        from orchestrations.ecom_orchestrator import execute_workflow
        await asyncio.create_task(execute_workflow())
        return {
            "message": "Voice chat workflow started",
            "session_id": session_id
        }
    
    except Exception as e:
        logger.exception(f"Error in API request routing", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(f"Error in API request routing: {str(e)}")
        )