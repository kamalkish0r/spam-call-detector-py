import logging
from sqlalchemy.orm import Session

from repository import user_repository

logger = logging.getLogger(__name__)


async def get_user_details(db: Session, user_id: int):
    logger.debug(f"find details of user : {user_id}")
    return user_repository.get_user_by_id(db=db, user_id=user_id)