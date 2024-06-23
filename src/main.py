from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.chat import chat_controller
from utils import app_lifespan

app = FastAPI(
    title="Bank AI API",
    description="Bank Assistant for interacting with customers",
    lifespan=app_lifespan,
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(chat_controller, prefix='/v1/chat', tags=["Chat"])