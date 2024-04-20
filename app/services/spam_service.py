from sqlalchemy.orm import Session
from models import Spam
from repository import spam_repository, user_repository

class SpamService():
    def report_spam(self, db: Session, spam_number: str, reporter_id: int):
        # Check if the user has already reported this spam number
        existing_spam = spam_repository.get_spam_by_number_and_reporter(db, spam_number, reporter_id)
        if existing_spam:
            return None 

        reporter = user_repository.get_user_by_id(db, reporter_id)
        if not reporter:
            return None  # Invalid reporter ID

        new_spam = Spam(spam_number=spam_number, reporter=reporter)
        return spam_repository.create_spam(db, new_spam)
    
    def is_spam(self, number: str):
        return False