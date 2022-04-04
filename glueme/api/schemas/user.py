from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, EmailStr, validator, constr

from glueme.api.schemas.tag import TagOut


class NickBase(BaseModel):
    nick: constr(regex=r'^(?=.{3,20}$)(?![0-9_])[a-zA-Z0-9_]+(?<![_.])$')


class PasswordBase(BaseModel):
    password: constr(regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$')


class UserAuthIn(BaseModel):
    nick_or_email: Union[str, EmailStr]
    password: str
    user_agent: str

    @validator('nick_or_email')
    def make_nick_or_email(cls, v):
        return v.strip()

    @validator('user_agent')
    def make_user_agent(cls, v):
        return v.strip()


class UserOut(BaseModel):
    id: int = Field()
    nick: str = Field()
    name: Optional[str] = Field()
    email: EmailStr = Field()
    created: datetime = Field()
    bio: Optional[str] = Field()
    tags: list[TagOut] = Field()

    class Config:
        orm_mode = True


class UserUpdateIn(BaseModel):
    name: Optional[str]
    bio: Optional[str]

    @validator('bio')
    def make_bio(cls, v):
        return v.strip() if v else v

    @validator('name')
    def make_name(cls, v):
        return v.strip() if v else v


class UserUpdateNickIn(NickBase):
    @validator('nick')
    def make_nick(cls, v):
        return v.strip() if v else v


class IsEmailExistsOut(BaseModel):
    exists: bool = Field()


class IsNickExistsOut(BaseModel):
    exists: bool = Field()
