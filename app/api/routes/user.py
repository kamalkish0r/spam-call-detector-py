import logging
from fastapi import APIRouter

from api.deps import SessionDep, CurrentUserDep
from services import user_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/profile")
async def get_user_data(
    db: SessionDep,
    user_id: CurrentUserDep
):
    return await user_service.get_user_details(db=db, user_id=user_id)