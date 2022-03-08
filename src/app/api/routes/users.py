from fastapi import APIRouter, Query, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.app.api.dependencies import get_session
from src.app.api.schemas.user import IsEmailExistsOut, IsNickExistsOut
from src.db import models

router = APIRouter()


@router.get('.is_email_exists', response_model=IsEmailExistsOut)
def is_email_exists(email: EmailStr = Query(...), s: Session = Depends(get_session)):
    email_exists = s.query(s.query(models.User).where(models.User.email == email).exists()).scalar()
    return IsEmailExistsOut(exists=email_exists)


@router.get('.is_nick_exists', response_model=IsNickExistsOut)
def is_email_exists(nick: str = Query(...), s: Session = Depends(get_session)):
    nick_exists = s.query(s.query(models.User).where(models.User.nick == nick).exists()).scalar()
    return IsNickExistsOut(exists=nick_exists)
