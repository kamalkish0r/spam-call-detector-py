import logging
from fastapi import APIRouter, Request
from models import get_db

from sqlalchemy.orm import Session
from fastapi import Depends
from services import spam_service
from schemas.spam import SpamStatus, MarkSpamResponse
from api.deps import SessionDep, CurrentUserDep

router = APIRouter(prefix="/contact-detail")
logger = logging.getLogger(__name__)


@router.put("/{contact_number}")
async def mark_as_spam(
    contact_number: str,
    db: SessionDep,
    user_id: CurrentUserDep
) -> MarkSpamResponse:
    try:
        spam_service.report_spam(db=db, spam_number=contact_number, reporter_id=int(user_id))
        return {'status': 'success'}
    except Exception as e:
        logger.error(e)
        return {'status': 'failure'}
    

@router.get("/{contact_number}")
async def get_spam_stutus(
    contact_number: str, 
    db: SessionDep,
    user_id: CurrentUserDep
) -> SpamStatus:
    status = spam_service.is_spam(db=db, number=contact_number)
    if status:
        return {"spam": True}
    return {"spam": False}