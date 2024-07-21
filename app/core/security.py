import logging
from datetime import timedelta
from typing import Any
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone

from core.config import settings
from exceptions import JWTCreationError, JWTValidationError
logger = logging.getLogger(__name__)


async def create_jwt_token(subject: str | Any, expire_delta: timedelta) -> str:
    try:
        expire = expire_delta + datetime.now(timezone.utc)
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except JWTError as je:
        error_msg = f"Error while creating JWT token for subject {subject}: {str(je)}"
        logger.error(error_msg)
        raise JWTCreationError(error_msg)
    

async def validate_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        if decoded_token['exp'] < datetime.now(timezone.utc).timestamp():
            logger.error("Token expired")
            return None
        
        return str(decoded_token["sub"])
    except ExpiredSignatureError as e:
        logger.error(f"Token signature expired. {str(e)}")
        raise JWTValidationError("Invalid JWT Token")
    except JWTError as e:
        logger.error(f"JWT decoding error. Invalid JWT Token: {e}")
        raise JWTValidationError("Invalid JWT Token")