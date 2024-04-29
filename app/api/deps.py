from fastapi import Depends
from typing import Annotated
from models import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

from services.auth_service import authorize_access_token

SessionDep = Annotated[Session, Depends(get_db)]
CurrentUserDep = Annotated[str, Depends(authorize_access_token)]