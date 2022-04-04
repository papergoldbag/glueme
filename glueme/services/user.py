import binascii
import os
from random import randint
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from glueme.models import models


class UserService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, password, hashed_password):
        return cls.pwd_context.verify(password, hashed_password)

    @classmethod
    def password_hash(cls, password):
        return cls.pwd_context.hash(password)

    @classmethod
    def generate_token(cls) -> str:
        res = binascii.hexlify(os.urandom(20)).decode() + str(randint(10000, 1000000))
        return res[:128]

    @classmethod
    def user_by_token(cls, s: Session, *, token: str) -> Optional[models.User]:
        return s.query(models.User, models.UserToken).filter(
            models.User.id == models.UserToken.user_id, models.UserToken.token == token
        ).scalar()

    @classmethod
    def user_has_tag_id(cls, s: Session, *, user_id: int, tag_id: int) -> bool:
        return s.query(s.query(models.TagToUser).where(
            models.TagToUser.tag_id == tag_id,
            models.TagToUser.user_id == user_id
        ).exists()).scalar()


