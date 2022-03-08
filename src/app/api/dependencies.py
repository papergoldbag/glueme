from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from src.db import models
from src.db.base import SessionLocal


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


http_bearer = HTTPBearer()


def get_current_user(ac: HTTPAuthorizationCredentials = Depends(http_bearer), s: Session = Depends(get_session)) -> models.User:
    token_value = ac.credentials
    user: Optional[models.User] = s.query(models.User, models.User).filter(models.User.id == models.UserToken.user_id, models.UserToken.token==token_value).scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='bad token')
    return user

