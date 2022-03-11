import binascii
import os
from datetime import datetime
from random import randint
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.db import models
from src.utils.normalizer import dt_to_utc


class UserService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def by_nick_or_email(cls, s: Session, *, nick_or_email: str) -> Optional[models.User]:
        return s.query(models.User).where(or_(models.User.nick == nick_or_email, models.User.email == nick_or_email)).scalar()

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
    def add_token(cls, s: Session, *, user_id: int, user_agent: str) -> models.UserToken:
        token = models.UserToken(
            token=cls.generate_token(),
            user_agent=user_agent,
            user_id=user_id
        )
        s.add(token)
        s.commit()
        return token

    @classmethod
    def email_exists(cls, s: Session, *, email: str) -> bool:
        return s.query(s.query(models.User).where(models.User.email == email).exists()).scalar()

    @classmethod
    def nick_exists(cls, s: Session, *, nick: str) -> bool:
        return s.query(s.query(models.User).where(models.User.nick == nick).exists()).scalar()

    @classmethod
    def add_user(cls, s: Session, *, nick: str, email: str, password: str) -> models.User:
        user = models.User(
            nick=nick,
            email=email,
            password_hash=cls.password_hash(password),
            created=dt_to_utc(datetime.now())
        )
        s.add(user)
        s.commit()
        return user

    @classmethod
    def by_token(cls, s: Session, *, token: str) -> Optional[models.User]:
        token = token.strip()
        return s.query(models.User, models.UserToken).filter(
            models.User.id == models.UserToken.user_id, models.UserToken.token == token
        ).scalar()

    @classmethod
    def has_tag_id(cls, s: Session, *, user_id: int, tag_id: int) -> bool:
        return s.query(s.query(models.UserTag).where(
            models.UserTag.tag_id == tag_id,
            models.UserTag.user_id == user_id
        ).exists()).scalar()

    @classmethod
    def tag_by_id(cls, s: Session, *, user_id: int, tag_id: int) -> Optional[models.UserTag]:
        return s.query(models.UserTag).where(
            models.UserTag.tag_id == tag_id,
            models.UserTag.user_id == user_id
        ).scalar()

