from pydantic import Field, EmailStr, validator, BaseModel, constr

from glueme.api.schemas.user import re_nick, re_password


class RegistrationIn(BaseModel):
    nick: constr(regex=re_nick)
    password: constr(regex=re_password)
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


class IsEmailExistsOut(BaseModel):
    exists: bool = Field()


class IsNickExistsOut(BaseModel):
    exists: bool = Field()

