from datetime import datetime, timedelta
from random import randint

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from src.app.api.dependencies import get_session
from src.app.api.schemas.code import CodeWasSent, SentCode, CodeValidity
from src.app.api.schemas.user import IsEmailExistsOut, IsNickExistsOut
from src.app.api.utils import dt_to_utc
from src.core.settings import settings
from src.db import models
from src.utils.emailsender import EmailSender

router = APIRouter()


def generate_code() -> str:
    return f'{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}'


@router.get('.send_code', response_model=CodeWasSent)
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
    return CodeWasSent(
        is_sent=True,
        sent_code=SentCode.from_orm(sent_code)
    )


@router.get('.is_valid', response_model=CodeValidity)
def is_valid(email: EmailStr = Query(...), code: str = Query(...), s: Session = Depends(get_session)):
    return CodeValidity(
        is_valid=s.query(s.query(models.Codes).where(
            models.Codes.email == email, models.Codes.code == code, models.Codes.expired > dt_to_utc(datetime.now())
        ).exists()).scalar()
    )


@router.get('.is_email_exists', response_model=IsEmailExistsOut)
def is_email_exists(email: EmailStr = Query(...), s: Session = Depends(get_session)):
    email_exists = s.query(s.query(models.User).where(models.User.email == email).exists()).scalar()
    return IsEmailExistsOut(exists=email_exists)


@router.get('.is_nick_exists', response_model=IsNickExistsOut)
def is_email_exists(nick: str = Query(...), s: Session = Depends(get_session)):
    nick_exists = s.query(s.query(models.User).where(models.User.nick == nick).exists()).scalar()
    return IsNickExistsOut(exists=nick_exists)

