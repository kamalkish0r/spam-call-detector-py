import logging
from datetime import timedelta
from typing import Any
from jose import jwt, JWTError
from datetime import datetime, timezone

from core.config import settings
logger = logging.getLogger(__name__)


async def create_jwt_token(subject: str | Any, expire_delta: timedelta) -> str:
    expire = expire_delta + datetime.now(timezone.utc)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def validate_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        if decoded_token['exp'] < datetime.now(timezone.utc).timestamp():
            logger.info("Token expired")
            return None
        
        return str(decoded_token["sub"])
    except JWTError as e:
        logger.error(f"JWT decoding error: {e}")
        return None