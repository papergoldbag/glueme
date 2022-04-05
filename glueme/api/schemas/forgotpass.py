from pydantic import BaseModel, constr, validator

from glueme.api.schemas.user import re_password


class UserForgotPass(BaseModel):
    code: str
    nick_or_email: str
    new_password: constr(regex=re_password)

    @validator('nick_or_email')
    def normalize_nick_or_email(cls, v):
        return v.strip()

    @validator('code')
    def normalize_code(cls, v):
        return v.strip()


class PasswordWasChanged(BaseModel):
    password_was_changed: bool
