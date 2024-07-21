import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from fastapi_limiter.depends import RateLimiter
from datetime import timedelta

from services import auth_service 
from schemas.auth import LoginRequest, TokenResponse
from repository import user_repository, token_repository
from core.security import create_jwt_token
from api.deps import SessionDep, CurrentUserDep
from core.config import settings
from exceptions import InvalidGoogleClientIDError, GoogleAuthError, JWTCreationError

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    '/login', 
    response_model=TokenResponse,
    dependencies=[Depends(RateLimiter(times=settings.MAX_LOGIN_REQUEST_COUNT, seconds=settings.RATE_LIMITING_SECONDS))]
)
async def login_via_google(
    db: SessionDep,
    request: LoginRequest
):
    try:
        user_data = await auth_service.authenticate_user(request.authToken)
        if not await auth_service.validate_google_client_id(user_data['aud']):
            logger.info("Google client ID does not match.")
            raise InvalidGoogleClientIDError("Invalid Google client ID.")
        
        user = await user_repository.get_or_create_user(db=db, user_dict=user_data)
        access_token = await create_jwt_token(
            subject=user.id, 
            expire_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        await token_repository.add_or_update_token(db=db, token=access_token, user_id=user.id)
        
        return TokenResponse(token=access_token)
    except GoogleAuthError or ValueError as e:
        logger.error(f"Google authentication failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid auth token.")
    except InvalidGoogleClientIDError as e:
        logger.error(f"Invalid Google client ID: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid auth token.")
    except JWTCreationError as e:
        logger.error(f"JWT creation failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    except Exception as e:
        logger.exception(f"Exception while processing user data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Internal Server Error"
        )
    
@router.post('/logout')
async def logout(
    db: SessionDep,
    user_id: CurrentUserDep
):
    try:
        result = await auth_service.handle_logout(db=db, user_id=int(user_id))
        if result:
            logger.info(f"User {user_id} logged out successfully")
            return {"status": "Success: Logged out"}
        else:
            logger.warning(f"Logout attempted for user {user_id}, but no active session was found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active session found")
    except ValueError as ve:
        logger.warning(f"Logout failed for user {user_id}: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error during logout for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="An unexpected error occurred"
        )
