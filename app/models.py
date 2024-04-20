from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    picture = Column(String)

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', picture='{self.picture}')"

class Spam(Base):
    __tablename__ = 'spam'

    id = Column(Integer, primary_key=True, index=True)
    spam_number = Column(String(10), unique=True)  
    reporter_id = Column(Integer, ForeignKey('users.id'))
    reporter = relationship('User', backref='reported_spam')

    def __repr__(self):
        return f"Spam(id={self.id}, spam_number='{self.spam_number}', reporter_id={self.reporter_id})"