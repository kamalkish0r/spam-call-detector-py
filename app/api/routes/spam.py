from fastapi import APIRouter, Request
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from services.spam_service import SpamService

spam_service = SpamService()
router = APIRouter(prefix="/contact-detail")

@router.put("/contact_number")
async def mark_as_spam(request: Request, contact_number: str, db: Session = Depends(get_db)):
    print(request.session.get('user'))
    # spam_service.report_spam(db=db, spam_number=contact_number)

@router.get("/contact_number")
async def get_stutus(request: Request, contact_number: str, db: Session = Depends(get_db)):
    print(request.session.get('user'))
