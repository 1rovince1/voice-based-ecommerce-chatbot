from fastapi import Header, HTTPException, status

from config import env_vars


async def verify_auth_api_key(chat_service_auth_key: str = Header(None)):
    CHAT_SERVICE_AUTH_KEY = env_vars.CHAT_SERVICE_API_AUTH_KEY
    
    if not chat_service_auth_key:
        raise RuntimeError("CHAT AUTH API key not configured")

    if chat_service_auth_key != CHAT_SERVICE_AUTH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )