import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Spam
from exceptions import SpamCreationError, SpamRetrievalError

logger = logging.getLogger(__name__)

async def create_spam(db: Session, spam: Spam):
    try:
        db.add(spam)
        db.commit()
        db.refresh(spam)
        return spam
    except SQLAlchemyError as e:
        logger.error(f"Error while creating spam: {str(e)}")
        db.rollback()
        raise SpamCreationError("Error while creating spam.")

async def get_spam_by_number_and_reporter(db: Session, spam_number: str, reporter_id: int):
    try:
        return db.query(Spam).filter(Spam.spam_number == spam_number, Spam.reporter_id == reporter_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error while retrieving spam by number and reporter: {str(e)}")
        raise SpamRetrievalError("Error while retrieving spam by number and reporter.")

async def get_spam_count(db: Session, spam_number: str) -> int:
    try:
        return db.query(Spam).filter(Spam.spam_number == spam_number).count()
    except SQLAlchemyError as e:
        logger.error(f"Error while counting spam: {str(e)}")
        raise SpamRetrievalError("Error while counting spam.")
