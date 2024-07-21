import logging
from fastapi import FastAPI
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from dotenv import load_dotenv
load_dotenv()

from api.main import api_router
from core.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url(settings.REDIS_URL, encoding="utf8")
    await FastAPILimiter.init(redis=redis_connection)
    yield
    await FastAPILimiter.close()

app = FastAPI(lifespan=lifespan)

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s - %(pathname)s:%(lineno)d - %(message)s'
)

app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)