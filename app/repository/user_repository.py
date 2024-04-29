from sqlalchemy.orm import Session

from models import User

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_or_create_user(db: Session, user_dict: dict) -> User:
    """
    Check if the user exists in the database based on the email or other
    unique identifier. If the user doesn't exist, create a new user.
    """
    user = get_user_by_email(db, user_dict.get('email'))
    if not user:
        user = User(
            name=user_dict['name'],
            email=user_dict['email'],
            picture=user_dict['picture']
        )
        create_user(db, user)

    return user