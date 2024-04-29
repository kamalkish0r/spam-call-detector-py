from fastapi import APIRouter

from .routes import auth, spam, user

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(spam.router, tags=["spam"])
api_router.include_router(user.router, tags=["user"])