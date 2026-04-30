from dotenv import load_dotenv
load_dotenv()
from config.logger_config import setup_logging
setup_logging()

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from api.routes.chat import router as ChatRouter
from api.utils.auth import verify_auth_api_key
from clients.ollama_client import ollama_manager
from clients.redis_client import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ollama_manager.connect()
    await redis_manager.connect()
    yield
    await ollama_manager.disconnect()
    await redis_manager.disconnect()


app = FastAPI(
    title="Voice-based E-commerce chatbot",
    lifespan=lifespan,
    dependencies=[Depends(verify_auth_api_key)]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(ChatRouter, tags=["Chat"])


@app.get("/")
async def health_check():
    return {
        "status": "ok",
        "message": "App passed health checks."
    }