from datetime import datetime

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from src.app.api.dependencies import get_session
from src.app.api.schemas.user import UserOut, UserCreateIn
from src.app.api.utils import make_http_exception, dt_to_utc, password_hash
from src.db import models

router = APIRouter()


@router.post('', response_model=UserOut)
async def user_reg(create_user: UserCreateIn = Body(...), s: Session = Depends(get_session)):
    is_valid_code = s.query(s.query(models.Codes).where(
        models.Codes.email == create_user.email,
        models.Codes.code == create_user.code,
        models.Codes.expired > dt_to_utc(datetime.now())
    ).exists()).scalar()
    if not is_valid_code:
        raise make_http_exception(['code'], 'code is invalid')

    email_exists = s.query(s.query(models.User).where(models.User.email == create_user.email).exists()).scalar()
    if email_exists:
        raise make_http_exception(['email'], 'email is exists')

    email_exists = s.query(s.query(models.User).where(models.User.nick == create_user.nick).exists()).scalar()
    if email_exists:
        raise make_http_exception(['nick'], 'nick is exists')

    user_data = create_user.dict()
    user = models.User(
        nick=user_data['nick'],
        name=user_data['name'],
        email=user_data['email'],
        password_hash=password_hash(create_user.password),
        created=dt_to_utc(datetime.now())
    )
    s.add(user)
    s.commit()

    return UserOut.from_orm(user)
