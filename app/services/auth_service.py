import httpx
import logging
from typing import Optional
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from core.security import validate_jwt_token
from core.config import settings
from repository import token_repository
from models import get_db
from exceptions import GoogleAuthError, JWTValidationError, DatabaseError


logger = logging.getLogger(__name__)

async def authenticate_user(auth_token: str) -> Optional[dict]:
    url = f'{settings.GOOGLE_OAUTH_API}={auth_token}'
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == status.HTTP_200_OK:
                user_data = response.json()
                if user_data:
                    return dict(user_data)
                
                error_msg = "No user details found in Google response."
                logger.error(error_msg)
                raise GoogleAuthError(error_msg)
            else:
                error_msg = f"Error fetching user details from Google: {response.status_code}, {response.json()}"
                logger.error(error_msg)
                raise GoogleAuthError(error_msg)
        except httpx.RequestError as exc:
            error_msg = f"Error fetching user details from Google: {str(exc)}"
            logger.error(error_msg)
            raise GoogleAuthError(error_msg)

async def get_access_token(access_token: Optional[str] = Header(None)):
    if not access_token or not access_token.startswith("Bearer "):
        logger.error("Access token missing or does not start with 'Bearer '.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    
    return access_token.split("Bearer ")[1]

async def authorize_access_token(
    db: Session = Depends(get_db),
    access_token: str = Depends(get_access_token)
):
    try:
        user_id = await validate_jwt_token(access_token)
        if not user_id:
            logger.error("User not found.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    
        token_in_db = await token_repository.find_token_by_user_id(db=db, user_id=user_id)
        if not token_in_db or token_in_db.token != access_token:
            logger.error("Token mismatch or not found in database.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
        
        return user_id
    except JWTValidationError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    except Exception as e:
        logger.error(f"Error validating access token: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")

async def validate_google_client_id(client_id: str) -> bool:
    try:
        return client_id == settings.GOOGLE_CLIENT_ID
    except Exception as e:
        error_msg = f"Error validating Google client ID: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)

async def handle_logout(db: Session, user_id: int):
    try:
        result = await token_repository.revoke_token(db=db, user_id=user_id)
        if result:
            return {"message": "Logout successful"}
        else:
            logger.warning(f"No active session found for user {user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active session found")
    except DatabaseError as e:
        logger.error(f"Database error revoking token for user {user_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
