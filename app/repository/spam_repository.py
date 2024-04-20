from sqlalchemy.orm import Session
from models import Spam

def create_spam(db: Session, spam: Spam):
    db.add(spam)
    db.commit()
    db.refresh(spam)
    return spam

def get_spam_by_number_and_reporter(db: Session, spam_number: str, reporter_id: int):
    return db.query(Spam).filter(Spam.spam_number == spam_number, Spam.reporter_id == reporter_id).first()

def get_spam_count(db: Session, spam_number: str):
    return db.query(Spam).filter(Spam.spam_number == spam_number).count()
