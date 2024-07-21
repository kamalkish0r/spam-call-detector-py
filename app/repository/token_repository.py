import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models import Token
from exceptions import TokenNotFoundError, TokenUpdateError, TokenCreationError, TokenDeletionError, DatabaseError

logger = logging.getLogger(__name__)

async def add_or_update_token(db: Session, token: str, user_id: int):
    try:
        return await update_token(db=db, token=token, user_id=user_id) or await add_token(db=db, token=token, user_id=user_id)
    except (TokenUpdateError, TokenCreationError) as e:
        logger.error(f"Error in add_or_update_token: {str(e)}")
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error in add_or_update_token: {str(e)}")
        raise DatabaseError("An error occurred while adding or updating the token")

async def update_token(db: Session, token: str, user_id: int):
    try:
        existing_token = await find_token_by_user_id(db=db, user_id=user_id)
        if existing_token:
            existing_token.token = token
            db.commit()
            logger.debug(f"Updated existing token to: {token}")
            return True
        logger.debug(f"No token present for user_id: {user_id}")
        return False
    except SQLAlchemyError as e:
        logger.error(f"Database error in update_token: {str(e)}")
        db.rollback()
        raise TokenUpdateError("An error occurred while updating the token")

async def add_token(db: Session, token: str, user_id: int):
    try:
        new_token = Token(token=token, user_id=user_id)
        db.add(new_token)
        db.commit()
        logger.debug(f"Added token to db: {token}")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database error in add_token: {str(e)}")
        db.rollback()
        raise TokenCreationError("An error occurred while creating the token")

async def find_token_by_user_id(db: Session, user_id: int):
    try:
        logger.debug(f"Finding token using user_id: {user_id}")
        return db.query(Token).filter(Token.user_id == user_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error in find_token_by_user_id: {str(e)}")
        raise TokenNotFoundError("An error occurred while finding the token")

async def find_token_by_token(db: Session, token: str):
    try:
        logger.debug(f"Finding token using token: {token}")
        return db.query(Token).filter(Token.token == token).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error in find_token_by_token: {str(e)}")
        raise TokenNotFoundError("An error occurred while finding the token")

async def revoke_token(db: Session, user_id: int) -> bool:
    try:
        result = db.query(Token).filter(Token.user_id == user_id).delete(synchronize_session=False)
        if result == 0:
            logger.warning(f"No token found for user {user_id}")
            return False
        db.commit()
        logger.info(f"Token removed successfully for user {user_id}")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database error while revoking token for user {user_id}: {str(e)}")
        db.rollback()
        raise TokenDeletionError("An error occurred while revoking the token")
