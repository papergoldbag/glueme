from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from ..app.db import new_session
from ..models import models
from ..services.user import UserService


def get_session():
    session = new_session()
    try:
        yield session
    finally:
        session.close()


http_bearer = HTTPBearer()


def get_current_user(ac: HTTPAuthorizationCredentials = Depends(http_bearer), s: Session = Depends(get_session)) -> models.User:
    user = UserService.user_by_token(s, token=ac.credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='bad token')
    return user

