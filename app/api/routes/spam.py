import logging
from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi_limiter.depends import RateLimiter

from api.deps import SessionDep, CurrentUserDep
from schemas.spam import SpamStatus, MarkSpamResponse, PhoneNumber
from services import spam_service
from core.config import settings


router = APIRouter(prefix="/contact-detail")
logger = logging.getLogger(__name__)


@router.put(
    "/mark_spam", 
    response_model=MarkSpamResponse,
    dependencies=[Depends(RateLimiter(times=settings.MAX_MARK_SPAM_REQUEST_COUNT, seconds=settings.RATE_LIMITING_SECONDS))]
)
async def mark_as_spam(
    contact_number: PhoneNumber,
    db: SessionDep,
    user_id: CurrentUserDep
) -> MarkSpamResponse:
    try:
        await spam_service.report_spam(db=db, spam_number=contact_number.number, reporter_id=int(user_id))
        return MarkSpamResponse(status='success')
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error while marking {contact_number.number} as spam by user {user_id}: {str(e)}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while marking number as spam.")


@router.post(
    "/spam_status",
    response_model=SpamStatus,
    dependencies=[Depends(RateLimiter(times=settings.MAX_GET_SPAM_STATUS_COUNT, seconds=settings.RATE_LIMITING_SECONDS))]
)
async def get_spam_stutus(
    contact_number: PhoneNumber, 
    db: SessionDep,
    current_user: CurrentUserDep
) -> SpamStatus:
    try:
        status = await spam_service.is_spam(db=db, number=contact_number.number)
        return SpamStatus(spam=status)
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error while fetching spam status for number {contact_number.number} : {str(e)}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while fetching spam status.") # todo : remove exact error and provide generic error