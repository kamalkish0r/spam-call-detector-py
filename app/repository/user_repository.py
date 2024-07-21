import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models import User
from exceptions import UserNotFoundError, UserCreationError, DatabaseError

logger = logging.getLogger(__name__)

async def get_user_by_id(db: Session, user_id: int):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error while find the user {user_id} : {str(e)}")
        raise UserNotFoundError("Error while finding user by id.")
    
async def get_user_by_email(db: Session, user_email: str):
    try:
        return db.query(User).filter(User.email == user_email).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving user by email {user_email} : {str(e)}")
        raise UserNotFoundError("Error while retrieving user by email id.")

async def create_user(db: Session, user: User):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while creating user {user} : {str(e)}")
        raise UserCreationError("Error while creating user.")

async def get_or_create_user(db: Session, user_dict: dict) -> User:
    """
    Check if the user exists in the database based on the email or other
    unique identifier. If the user doesn't exist, create a new user.
    """
    try:
        user = await get_user_by_email(db, user_dict.get('email'))
        if not user:
            user = User(
                name=user_dict['name'],
                email=user_dict['email'],
                picture=user_dict['picture']
            )
            await create_user(db, user)

        return user
    except SQLAlchemyError or DatabaseError as e:
        logger.error(f"Database error for get or create user {user_dict} : {str(e)}")
        raise DatabaseError("Error while getting or creating user.")