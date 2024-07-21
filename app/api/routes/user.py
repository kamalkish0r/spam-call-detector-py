import logging
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from api.deps import SessionDep, CurrentUserDep
from services import user_service
from core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)



@router.get("/profile", dependencies=[Depends(
    RateLimiter(times=settings.MAX_GET_PROFILE_DETAILS_COUNT, seconds=settings.RATE_LIMITING_SECONDS))])
async def get_user_data(
    db: SessionDep,
    user_id: CurrentUserDep
):
    return await user_service.get_user_details(db=db, user_id=user_id)