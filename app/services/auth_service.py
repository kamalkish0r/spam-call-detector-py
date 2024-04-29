import httpx
import logging
from typing import Optional
from fastapi import Depends, Header, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK 
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv(".oauth_env")

from core.security import validate_jwt_token
from core.config import settings
from repository import token_repository
from models import get_db


logger = logging.getLogger(__name__)

async def authenticate_user(auth_token: str) -> Optional[dict]:
    url = f'{settings.GOOGLE_OAUTH_API}={auth_token}'
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == HTTP_200_OK:
                user_data = response.json()
                return dict(user_data) if user_data else None
            else:
                return None
        except httpx.RequestError as exc:
            logger.error(exc)
            return None
        
async def get_access_token(access_token: Optional[str] = Header(None)):
    if not access_token or not access_token.startswith("Bearer "):
        logger.error("Either access token not passed or it doesn't start with Bearer.")
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    return access_token.split("Bearer ")[1]

async def authorize_access_token(
    db: Session = Depends(get_db),
    access_token: str = Depends(get_access_token)
):
    user_id = await validate_jwt_token(access_token)
    if not user_id:
        logger.error("User doesn't exist.")
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    
    token_in_db = token_repository.find_token(db=db, user_id=user_id).token
    if token_in_db != access_token:
        logger.error("Token doesn't match with one present in database.")
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    
    return user_id

async def validate_google_client_id(client_id: str) -> bool:
    if client_id == os.getenv("GOOGLE_CLIENT_ID"):
        return True
    
    logger.error("Invalid Google Client ID.")
    return False

async def handle_logout(db: Session, user_id):
    """
    Remove the token 
    """
    return token_repository.revoke_token(db=db, user_id=user_id)