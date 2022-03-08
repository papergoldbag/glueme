from datetime import datetime

import pytz
from fastapi import HTTPException
from passlib.context import CryptContext


def make_http_exception(loc: list[str], msg: str = None) -> HTTPException:
    return HTTPException(
        422,
        [{
            'loc': loc,
            'msg': msg
        }]
    )


def dt_to_utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=None).astimezone(pytz.UTC).replace(tzinfo=None)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def password_hash(password):
    return pwd_context.hash(password)

