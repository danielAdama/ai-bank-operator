from fastapi import FastAPI
import redis
from contextlib import asynccontextmanager
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
import os

def get_redis_client():
    return redis.Redis(
        host=os.environ.get("REDIS_HOST"), 
        port=int(os.environ.get("REDIS_PORT")),
        # db=os.environ.get("REDIS_DB"),
        password=os.environ.get("REDIS_PASSWORD")
    )

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    app.state.redis_client = get_redis_client()
    
    try:
        yield
    finally:
        app.state.redis_client.flushdb()
        app.state.redis_client.close()