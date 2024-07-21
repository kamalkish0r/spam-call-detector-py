import logging
from sqlalchemy.orm import Session

from repository import user_repository
from schemas.user import UserDetails

logger = logging.getLogger(__name__)


async def get_user_details(db: Session, user_id: int) -> UserDetails:
    logger.debug(f"find details of user : {user_id}")
    user = user_repository.get_user_by_id(db=db, user_id=user_id)
    user_details = UserDetails(
        name=user.name,
        email=user.email,
        picture=user.picture
    )
    logger.debug(f"User details : {user_details}")
    return user_details