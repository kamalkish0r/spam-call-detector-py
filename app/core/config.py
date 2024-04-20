from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import secrets
from pydantic_settings import BaseSettings

config = Config('.oauth_env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

class Settings(BaseSettings):
    SECRET_KEY = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM = "HS256"
    SQLALCHEMY_DATABASE_URI="sqlite:///./sql_app.db"

settings = Settings()