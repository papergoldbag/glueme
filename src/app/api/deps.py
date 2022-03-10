from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from src.db import models
from src.db.base import SessionLocal
from src.services.user import UserService


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


http_bearer = HTTPBearer()


def get_current_user(ac: HTTPAuthorizationCredentials = Depends(http_bearer), s: Session = Depends(get_session)) -> models.User:
    user = UserService.by_token(s, token=ac.credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='bad token')
    return user

