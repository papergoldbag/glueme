from pydantic import BaseModel, constr

from glueme.api.schemas.user import re_password


class UserForgotPass(BaseModel):
    code: str
    nick_or_email: str
    new_password: constr(regex=re_password)


class PasswordWasChanged(BaseModel):
    password_was_changed: bool
