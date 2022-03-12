from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.app.api.deps import get_session
from src.app.api.schemas.user import IsEmailExistsOut, IsNickExistsOut
from src.services.user import UserService

router = APIRouter()


@router.get('.is_email_exists', response_model=IsEmailExistsOut)
def is_email_exists(email: EmailStr = Query(...), s: Session = Depends(get_session)):
    return IsEmailExistsOut(exists=UserService.email_exists(s, email=email))


@router.get('.is_nick_exists', response_model=IsNickExistsOut)
def is_nick_exists(nick: str = Query(...), s: Session = Depends(get_session)):
    return IsNickExistsOut(exists=UserService.nick_exists(s, nick=nick))
