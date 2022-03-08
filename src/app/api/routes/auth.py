import binascii
import os
from random import randint

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status

from src.app.api.dependencies import get_session
from src.app.api.schemas.token import TokenOut
from src.app.api.schemas.user import UserAuth
from src.app.api.utils import verify_password
from src.db import models

router = APIRouter()


def generate_token() -> str:
    res = binascii.hexlify(os.urandom(20)).decode() + str(randint(10000, 1000000))
    return res[:128]


@router.post('', response_model=TokenOut)
def auth(user_auth: UserAuth = Body(...), s: Session = Depends(get_session)):
    user = s.query(models.User).where(or_(
        models.User.nick == user_auth.nick_or_email, models.User.email == user_auth.nick_or_email,
    )).scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='bad auth data')
    if not verify_password(user_auth.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='bad auth data')

    token = models.UserToken(
        token=generate_token(),
        user_agent=user_auth.user_agent,
        user_id=user.id
    )
    s.add(token)
    s.commit()
    return TokenOut.from_orm(token)

