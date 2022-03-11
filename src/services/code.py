from datetime import datetime, timedelta
from random import randint

from sqlalchemy.orm import Session

from src.core.settings import settings
from src.db import models
from src.utils.emailsender import EmailSender
from src.utils.normalizer import dt_to_utc


class CodeService:
    email_sender = EmailSender()

    @classmethod
    def is_valid_code(cls, s: Session, *, email: str, code: str) -> bool:
        return s.query(s.query(models.Code).where(
            models.Code.email == email,
            models.Code.code == code,
            models.Code.expired > dt_to_utc(datetime.now()),
            models.Code.is_used == False
        ).exists()).scalar()

    @classmethod
    def generate_code(cls) -> str:
        return f'{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}'

    @classmethod
    def add_code(cls, s: Session, *, email: str, code: str) -> models.Code:
        sent_code = models.Code(
            code=code,
            email=email,
            created=dt_to_utc(datetime.now()),
            expired=dt_to_utc(datetime.now() + timedelta(seconds=settings.max_sec_code_reg)),
            is_used=False
        )
        s.add(sent_code)
        s.commit()
        return sent_code

    @classmethod
    def deactivate_code(cls, s: Session, *, email: str, code: str):
        code: models.Code = s.query(s.query(models.Code).where(
            models.Code.email == email,
            models.Code.code == code,
            models.Code.expired > dt_to_utc(datetime.now()),
            models.Code.is_used == False
        ).exists()).scalar()
        if not code:
            return
        code.is_used = True
        s.commit()
