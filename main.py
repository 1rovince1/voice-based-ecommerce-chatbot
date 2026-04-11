from config.logger_config import setup_logging
setup_logging()
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from api.routes.chat import router as ChatRouter
from api.utils.auth import verify_auth_api_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


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