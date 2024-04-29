from sqlalchemy.orm import Session
import logging

from models import Token

logger = logging.getLogger(__name__)


def add_or_update_token(db: Session, token: str, user_id: int):
    existing_token = find_token(db=db, user_id=user_id)
    
    if existing_token:
        existing_token.token = token
        db.commit() 
        logger.debug(f"updated existing token to : {token}")
    else:
        new_token = Token(token=token, user_id=user_id)
        db.add(new_token)
        db.commit() 
        logger.debug(f"added token to db : {token}")

def find_token(db: Session, token: str):
    logger.debug(f"find_token using token {token}")
    return db.query(Token).filter(Token.token == token).first()

def find_token(db: Session, user_id: int):
    logger.debug(f"find_token using user_id {user_id}")
    return db.query(Token).filter(Token.user_id == user_id).first()