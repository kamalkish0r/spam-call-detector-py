import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi_limiter.depends import RateLimiter
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import timedelta

from services import auth_service 
from schemas.auth import LoginRequest, TokenResponse
from repository import user_repository, token_repository
from core.security import create_jwt_token
from api.deps import SessionDep, CurrentUserDep
from core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/login', 
             response_model=TokenResponse,
             dependencies=[Depends(RateLimiter(times=settings.MAX_LOGIN_REQUEST_COUNT, seconds=settings.RATE_LIMITING_SECONDS))])
async def login_via_google(
    db: SessionDep,
    request: LoginRequest
):
    # Todo : handle 400 bad request when expired authToken is passed to google
    user_data = await auth_service.authenticate_user(request.authToken)
    if user_data:
        if not await auth_service.validate_google_client_id(user_data['aud']):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not authenticated")
        
        user = user_repository.get_or_create_user(db=db, user_dict=user_data)
        access_token = await create_jwt_token(subject=user.id, expire_delta=timedelta(days=15))
        token_repository.add_or_update_token(db=db, token=access_token, user_id=user.id)
        
        return TokenResponse(token=access_token)
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    
@router.get('/logout')
async def logout(
    db: SessionDep,
    user_id: str = CurrentUserDep
):
    # Todo : better handling
    if auth_service.handle_logout(db=db, user_id=user_id):
        return {"status": "Success : Logged out"}
    return HTTPException(HTTP_401_UNAUTHORIZED, detail="User not authorised")