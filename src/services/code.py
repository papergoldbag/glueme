from datetime import datetime, timedelta
from random import randint
from typing import Optional

from sqlalchemy.orm import Session

from src.glueme import models
from src.glueme.settings import DELAY_BETWEEN_REG_CODES, LIFETIME_REG_CODE, DELAY_BETWEEN_FORGOTPASS_CODES, \
    LIFETIME_FORGOTPASS_CODE
from src.utils.dtutc import dt_to_utc


class CodeService:
    def __init__(self, auto_commit: bool = True):
        self.is_auto_commit = auto_commit

    @classmethod
    def _get_last_code(cls, s: Session, *, email: str, code_type_name: str) -> Optional[models.SentCode]:
        return s.query(models.SentCode).where(
            models.SentCode.email == email,
            models.SentCode.code_type_name == code_type_name
        ).order_by(models.SentCode.created.desc()).first()

    @classmethod
    def _can_send(cls, s: Session, *, email: str, code_type_name: str, delay: int) -> bool:
        code: Optional[models.SentCode] = cls._get_last_code(
            s,
            email=email,
            code_type_name=code_type_name
        )
        if not code:
            return True
        if code:
            if (dt_to_utc(datetime.now()) - code.created).seconds > delay:
                return True
        return False

    @classmethod
    def can_send_reg_code(cls, s: Session, *, email: str) -> bool:
        return cls._can_send(
            s,
            email=email,
            code_type_name=models.CodeType.Types.REG,
            delay=DELAY_BETWEEN_REG_CODES
        )

    @classmethod
    def can_send_forgotpass_code(cls, s: Session, *, email: str) -> bool:
        return cls._can_send(
            s,
            email=email,
            code_type_name=models.CodeType.Types.FORGOT_PASS,
            delay=DELAY_BETWEEN_FORGOTPASS_CODES
        )

    @classmethod
    def get_valid_code(cls, s: Session, *, email: str, code: str, code_type_name: str) -> Optional[models.SentCode]:
        found_code: Optional[models.SentCode] = cls._get_last_code(
            s, email=email, code_type_name=code_type_name
        )
        if found_code \
                and found_code.code == code \
                and found_code.expired > dt_to_utc(datetime.now()) \
                and not found_code.is_used:
            return found_code
        return None

    @classmethod
    def is_valid_reg_code(cls, s: Session, *, email: str, code: str) -> bool:
        code = cls.get_valid_code(
            s,
            email=email,
            code=code,
            code_type_name=models.CodeType.Types.REG
        )
        return True if code else False

    @classmethod
    def is_valid_forgotpass_code(cls, s: Session, *, email: str, code: str) -> bool:
        code = cls.get_valid_code(
            s,
            email=email,
            code=code,
            code_type_name=models.CodeType.Types.FORGOT_PASS
        )
        return True if code else False

    @classmethod
    def generate_code(cls) -> str:
        return f'{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}'

    @classmethod
    def _add_code(cls, s: Session, *, email: str, code: str, code_type_name: str, lifetime: int) -> models.SentCode:
        sent_code = models.SentCode(
            code=code,
            email=email,
            created=dt_to_utc(datetime.now()),
            expired=dt_to_utc(datetime.now() + timedelta(seconds=lifetime)),
            is_used=False,
            code_type_name=code_type_name
        )
        s.add(sent_code)
        s.commit()
        return sent_code

    @classmethod
    def add_reg_code(cls, s: Session, *, email: str, code: str):
        return cls._add_code(
            s,
            email=email,
            code=code,
            code_type_name=models.CodeType.Types.REG,
            lifetime=LIFETIME_REG_CODE
        )

    @classmethod
    def add_forgotpass_code(cls, s: Session, *, email: str, code: str):
        return cls._add_code(
            s,
            email=email,
            code=code,
            code_type_name=models.CodeType.Types.FORGOT_PASS,
            lifetime=LIFETIME_FORGOTPASS_CODE
        )

