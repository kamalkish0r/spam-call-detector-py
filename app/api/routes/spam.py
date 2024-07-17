import logging
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from api.deps import SessionDep, CurrentUserDep
from schemas.spam import SpamStatus, MarkSpamResponse, PhoneNumber
from services import spam_service

router = APIRouter(prefix="/contact-detail")
logger = logging.getLogger(__name__)


@router.put("/mark_spam", response_model=MarkSpamResponse)
async def mark_as_spam(
    contact_number: PhoneNumber,
    db: SessionDep,
    user_id: CurrentUserDep
) -> MarkSpamResponse:
    try:
        spam_service.report_spam(db=db, spam_number=contact_number.number, reporter_id=int(user_id))
        return MarkSpamResponse(status='success')
    except Exception as e:
        logger.error(f"Error while marking {contact_number.number} as spam by user {user_id}: {str(e)}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while marking number as spam.")

@router.post("/spam_status")
async def get_spam_stutus(
    contact_number: PhoneNumber, 
    db: SessionDep,
    current_user: CurrentUserDep
) -> SpamStatus:
    try:
        status = spam_service.is_spam(db=db, number=contact_number.number)
        return SpamStatus(spam=status)
    except Exception as e:
        logger.error(f"Error while fetching spam status for number {contact_number.number} : {str(e)}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while fetching spam status.") # todo : remove exact error and provide generic error