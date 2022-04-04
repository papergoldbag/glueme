from pydantic import Field, EmailStr, validator

from glueme.api.schemas.user import NickBase, PasswordBase


class RegistrationIn(NickBase, PasswordBase):
    email: EmailStr
    code: str
    tag_ids: list[int] = Field(min_items=3)

    @validator('code')
    def make_code(cls, v):
        return v.strip()

    @validator('nick')
    def make_nick(cls, v):
        return v.strip()

    @validator('email')
    def make_email(cls, v):
        return v.strip()
