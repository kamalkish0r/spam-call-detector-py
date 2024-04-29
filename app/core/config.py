from pydantic_settings import BaseSettings
from typing import ClassVar
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: ClassVar[str] = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"
    SPAM_REPPORT_LIMIT:int = 100
    GOOGLE_OAUTH_API:str = "https://oauth2.googleapis.com/tokeninfo?id_token"

settings = Settings()
