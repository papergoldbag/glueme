from fastapi import APIRouter, Query, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.app.api.deps import get_session
from src.app.api.schemas.code import CodeValidityOut, SentCodeStatusOut
from src.services.code import CodeService

router = APIRouter()


@router.get('.send', response_model=SentCodeStatusOut)
def send_code(email: EmailStr = Query(...), s: Session = Depends(get_session)):
    CodeService.send_code(s, email)
    return SentCodeStatusOut(is_sent=True)


@router.get('.is_valid', response_model=CodeValidityOut)
def is_valid(email: EmailStr = Query(...), code: str = Query(...), s: Session = Depends(get_session)):
    return CodeValidityOut(is_valid=CodeService.is_valid_code(s, email=email, code=code))


