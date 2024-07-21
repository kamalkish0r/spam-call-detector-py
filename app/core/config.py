from pydantic_settings import BaseSettings
from typing import ClassVar
import os


class Settings(BaseSettings):
    SECRET_KEY: ClassVar[str] = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"
    SPAM_REPPORT_LIMIT:int = 100
    GOOGLE_OAUTH_API:str = "https://oauth2.googleapis.com/tokeninfo?id_token"
    
    # Rate limiting settings
    MAX_LOGIN_REQUEST_COUNT: int = int(os.getenv('MAX_LOGIN_REQUEST_COUNT', '2')) 
    MAX_MARK_SPAM_REQUEST_COUNT: int = int(os.getenv('MAX_MARK_SPAM_REQUEST_COUNT', '5'))
    MAX_GET_SPAM_STATUS_COUNT: int = int(os.getenv('MAX_GET_SPAM_STATUS_COUNT', '10'))
    MAX_GET_PROFILE_DETAILS_COUNT: int = int(os.getenv('MAX_GET_PROFILE_DETAILS_COUNT', '10'))
    RATE_LIMITING_SECONDS: int = int(os.getenv('RATE_LIMITING_SECONDS', '5'))

    # Redis settings
    REDIS_URL: str = os.getenv('REDIS_URL', "redis://127.0.0.1:6379")

settings = Settings()
