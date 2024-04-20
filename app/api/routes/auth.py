import logging
from typing import Optional

from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from services.auth_service import AuthService
from core.config import oauth

router = APIRouter()
auth_service = AuthService(oauth)

@router.get('/login')
async def login_via_google(request: Request):
    """
    Initiate the Google authentication flow by redirecting the user to the Google login page.

    Args:
        request (Request): The incoming request object.

    Returns:
        RedirectResponse: A redirect response to the Google login page.
    """
    redirect_uri = request.url_for('auth_via_google')
    return await auth_service.authorize_redirect(request, redirect_uri)

@router.get('/auth')
async def auth_via_google(request: Request):
    """
    Handle the Google authentication callback and retrieve the user information.

    Args:
        request (Request): The incoming request object.

    Returns:
        JSONResponse: A JSON response containing the user information or an error message.
    """
    try:
        user = await auth_service.authorize_access_token(request)
        if user:
            user = auth_service.success_response(user)
            request.session['user'] = user
            return user
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Failed to get user information")
    except Exception as e:
        logging.error(f"Authentication error: {e}")
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=str(e))

@router.get("/profile")
async def get_user_details(request: Request):
    """
    Retrieve the authenticated user's details.

    Args:
        request (Request): The incoming request object.

    Returns:
        JSONResponse: A JSON response containing the user details or an error message.
    """
    user = request.session.get('user')
    if user:
        return auth_service.success_response(user)
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not authenticated")

@router.get('/logout')
async def logout(request: Request):
    """
    Log out the authenticated user by clearing the session.

    Args:
        request (Request): The incoming request object.

    Returns:
        RedirectResponse: A redirect response to the root URL.
    """
    request.session.pop('user', None)
    return RedirectResponse(url='/')