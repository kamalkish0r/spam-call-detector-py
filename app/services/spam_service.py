import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import status

from models import Spam
from core.config import settings
from repository import spam_repository, user_repository
from exceptions import UserNotFoundError, DatabaseError

logger = logging.getLogger(__name__)

async def report_spam(db: Session, spam_number: str, reporter_id: int):
    try:
        existing_spam = await spam_repository.get_spam_by_number_and_reporter(db, spam_number, reporter_id)
        if existing_spam:
            logger.info(f"{spam_number} already reported as spam by the reporter id : {reporter_id}")
            return None 

        reporter = await user_repository.get_user_by_id(db, reporter_id)
        if not reporter:
            logger.error(f"Reporter ID '{reporter_id}' not found.")
            raise UserNotFoundError("Reporter not found. Invalid reporter ID")

        new_spam = Spam(spam_number=spam_number, reporter_id=reporter_id)
        return await spam_repository.create_spam(db, new_spam)
    except DatabaseError as e:
        logger.error(f"Database Error while reporting spam : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error.")
    
async def is_spam(db: Session, number: str):
    try:
        return await spam_repository.get_spam_count(db=db, spam_number=number) >  settings.SPAM_REPPORT_THRESHOLD
    except DatabaseError as e:
        logger.error(f"Database Error while retrieving spam details for {number} : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error.")
    