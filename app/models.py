from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

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

    def __repr__(self):
        return f"Spam(id={self.id}, spam_number='{self.spam_number}', reporter_id={self.reporter_id})"

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)  
    token = Column(String(255), unique=True, nullable=False) 

    def __repr__(self):
        return f'Token(id={self.id}, token={self.token}, user_id={self.user_id})'    
    
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Step 3: Declare Base Model
Base.metadata.reflect(bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
