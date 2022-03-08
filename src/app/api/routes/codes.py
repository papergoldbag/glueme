from datetime import datetime, timedelta
from random import randint

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from src.app.api.dependencies import get_session
from src.app.api.schemas.code import SentCodeOut, CodeValidityOut
from src.app.api.utils import dt_to_utc
from src.core.settings import settings
from src.db import models
from src.utils.emailsender import EmailSender

router = APIRouter()


def generate_code() -> str:
    return f'{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}'


@router.get('.send', response_model=SentCodeOut)
def send_code(email: str, session: Session = Depends(get_session)):
    code = generate_code()
    try:
        EmailSender.send_simple_message([email], 'Send Code', code)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='cannot send email')
    sent_code = models.Codes(
        code=code,
        email=email,
        created=dt_to_utc(datetime.now()),
        expired=dt_to_utc(datetime.now() + timedelta(seconds=settings.max_sec_code_reg)),
        is_active=True
    )
    session.add(sent_code)
    session.commit()
    return SentCodeOut.from_orm(sent_code)


@router.get('.is_valid', response_model=CodeValidityOut)
def is_valid(email: EmailStr = Query(...), code: str = Query(...), s: Session = Depends(get_session)):
    return CodeValidityOut(
        is_valid=s.query(s.query(models.Codes).where(
            models.Codes.email == email, models.Codes.code == code, models.Codes.expired > dt_to_utc(datetime.now())
        ).exists()).scalar()
    )


