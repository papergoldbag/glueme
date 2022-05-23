from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from ..glueme import models
from ..glueme.db import new_session
from ..services.user import UserService


def get_session():
    session = new_session()
    try:
        yield session
    finally:
        session.close()


http_bearer = HTTPBearer()
# api_key_header = APIKeyHeader(name='apikey', auto_error=True)


# def check_api_key(apikey: str = Security(api_key_header)):
#     if apikey != APIKEY:
#         raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authenticated")


def get_current_user(ac: HTTPAuthorizationCredentials = Security(http_bearer), s: Session = Depends(get_session)) -> models.User:
    user = UserService.user_by_token(s, token=ac.credentials)
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authenticated")
    return user

