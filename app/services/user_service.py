import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repository import user_repository
from schemas.user import UserDetails
from exceptions import DatabaseError

logger = logging.getLogger(__name__)


async def get_user_details(db: Session, user_id: int) -> UserDetails:
    try:
        logger.debug(f"find details of user : {user_id}")
        user = await user_repository.get_user_by_id(db=db, user_id=user_id)
        user_details = UserDetails(
            name=user.name,
            email=user.email,
            picture=user.picture
        )
        logger.debug(f"User details : {user_details}")
        return user_details
    except DatabaseError as e:
        logger.error(f"Database error while fetching user details for {user_id} : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error.")
