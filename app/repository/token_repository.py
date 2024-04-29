from sqlalchemy.orm import Session
import logging

from models import Token

logger = logging.getLogger(__name__)


def add_or_update_token(db: Session, token: str, user_id: int):
    return update_token(db=db, token=token, user_id=user_id) or add_token(db=db, token=token, user_id=user_id)        

def update_token(db: Session, token: str, user_id: int):
    existing_token = find_token(db=db, user_id=user_id)
    
    if existing_token:
        existing_token.token = token
        db.commit() 
        logger.debug(f"updated existing token to : {token}")
        return True
    
    logger.debug(f"No token present for user_id : {user_id}")
    return False

def add_token(db: Session, token: str, user_id: int):
    new_token = Token(token=token, user_id=user_id)
    db.add(new_token)
    db.commit() 
    logger.debug(f"added token to db : {token}")
    return True

def find_token(db: Session, token: str):
    logger.debug(f"find_token using token {token}")
    return db.query(Token).filter(Token.token == token).first()

def find_token(db: Session, user_id: int):
    logger.debug(f"find_token using user_id {user_id}")
    return db.query(Token).filter(Token.user_id == user_id).first()

def revoke_token(db: Session, user_id: int) -> bool:
    logger.debug(f"Revoke token for user : {user_id}")
    try:
        # Query the Token table for the entry associated with the user ID
        token = db.query(Token).filter(Token.user_id == user_id).first()
        
        if token:
            # If the token exists, delete it from the database
            db.delete(token)
            db.commit()
            logger.debug("Token removed successfully.")
        else:
            logger.debug("Token not found for the user.")
        
        return True
    except Exception as e:
        logger.error(f"An error occurred while removing token for user {user_id}: {e}")
        db.rollback()
        return False