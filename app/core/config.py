from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Security settings
    SECRET_KEY: str = os.getenv('SECRET_KEY', '')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"

    # Database settings
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL', "sqlite:///./sql_app.db")

    # API settings
    GOOGLE_OAUTH_API: str = "https://oauth2.googleapis.com/tokeninfo?id_token"

    # Rate limiting settings
    MAX_LOGIN_REQUEST_COUNT: int = int(os.getenv('MAX_LOGIN_REQUEST_COUNT', '2')) 
    MAX_MARK_SPAM_REQUEST_COUNT: int = int(os.getenv('MAX_MARK_SPAM_REQUEST_COUNT', '5'))
    MAX_GET_SPAM_STATUS_COUNT: int = int(os.getenv('MAX_GET_SPAM_STATUS_COUNT', '10'))
    MAX_GET_PROFILE_DETAILS_COUNT: int = int(os.getenv('MAX_GET_PROFILE_DETAILS_COUNT', '10'))
    RATE_LIMITING_SECONDS: int = int(os.getenv('RATE_LIMITING_SECONDS', '5'))
    RATE_LIMITING_SECONDS: int = int(os.getenv('RATE_LIMITING_SECONDS', '5'))

    # Redis settings
    REDIS_URL: str = os.getenv('REDIS_URL', "redis://127.0.0.1:6379")

    def dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()