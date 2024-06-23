from fastapi import FastAPI
import redis
from contextlib import asynccontextmanager
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
import os

print(os.environ.get("REDIS_HOST"))
print(int(os.environ.get("REDIS_PORT")))
print(int(os.environ.get("REDIS_DB")))

def get_redis_client():
    return redis.Redis(
        host=os.environ.get("REDIS_HOST"), 
        port=int(os.environ.get("REDIS_PORT")), 
        db=int(os.environ.get("REDIS_DB"))
    )

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    app.state.redis_client = get_redis_client()
    
    try:
        yield
    finally:
        app.state.redis_client.flushdb()
        app.state.redis_client.close()