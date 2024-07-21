import logging
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi_limiter.depends import RateLimiter

from api.deps import SessionDep, CurrentUserDep
from services import user_service
from core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)



@router.get(
    "/profile", 
    dependencies=[Depends(RateLimiter(times=settings.MAX_GET_PROFILE_DETAILS_COUNT, seconds=settings.RATE_LIMITING_SECONDS))]
)
async def get_user_data(
    db: SessionDep,
    user_id: CurrentUserDep
):
    try:
        return await user_service.get_user_details(db=db, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error.")