import logging
from sqlalchemy.orm import Session
from models import Spam
from core.config import settings
from repository import spam_repository, user_repository

logger = logging.getLogger(__name__)

def report_spam(db: Session, spam_number: str, reporter_id: int):
    existing_spam = spam_repository.get_spam_by_number_and_reporter(db, spam_number, reporter_id)
    if existing_spam:
        logger.info(f"{spam_number} already reported as spam by the reporter id : {reporter_id}")
        return None 

    reporter = user_repository.get_user_by_id(db, reporter_id)
    if not reporter:
        logger.error(f"Reporter ID '{reporter_id}' not found.")
        raise Exception("Invalid reporter ID")

    new_spam = Spam(spam_number=spam_number, reporter_id=reporter_id)
    return spam_repository.create_spam(db, new_spam)

def is_spam(db: Session, number: str):
    return spam_repository.get_spam_count(db=db, spam_number=number) >  settings.SPAM_REPPORT_LIMIT
