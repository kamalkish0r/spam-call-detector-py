from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends
from authlib.integrations.starlette_client import OAuthError
from starlette.requests import Request
from starlette.responses import JSONResponse

from core import security
from database import get_db
from repository import user_repository
from models import User


class AuthService:
    def __init__(self, oauth):
        self.oauth = oauth

    async def authorize_redirect(self, request: Request, redirect_uri: str):
        return await self.oauth.google.authorize_redirect(request, redirect_uri)

    async def authorize_access_token(self, request: Request) -> Optional[dict]:
        try:
            token = await self.oauth.google.authorize_access_token(request)
            user = token.get('userinfo')
            return dict(user) if user else None
        except OAuthError as e:
            raise e
# {"iss": "https://accounts.google.com", "azp": "174594637674-ne7lnol93jd9csrv85ss974rpgaipvet.apps.googleusercontent.com", "aud": "174594637674-ne7lnol93jd9csrv85ss974rpgaipvet.apps.googleusercontent.com", "sub": "107913324862626044178", "email": "notkamalkishor@gmail.com", "email_verified": true, "at_hash": "Yx_fkByqjoHtSkQkT4VbWA", "nonce": "JbAC2ivWCUMK3OZ5Tozf", "name": "Kamal Kishor", "picture": "https://lh3.googleusercontent.com/a/ACg8ocKTPZwiWm7GiADn6QUIngfBtvDMQJu0GVo-BvWABywFEiPeahg=s96-c", "given_name": "Kamal", "family_name": "Kishor", "iat": 1712986106, "exp": 1712989706}

    def success_response(self, user: dict, db: Session = Depends(get_db)):
        existing_user = user_repository.get_user_by_email(user['email'])
        access_token = security.create_access_token(user['sub'], user['exp'])
        if existing_user:
            return {"access_token": access_token}
        
        new_user = User(
            name=user['name'],
            email=user['email'],
            picture=user['picture']
        )
        user_repository.create_user(db, new_user)
        return {"access_token": access_token}
