from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, EmailStr, validator

from src.app.api.schemas.tag import TagOut


class UserAuthIn(BaseModel):
    nick_or_email: Union[str, EmailStr] = Field()
    password: str = Field()
    user_agent: str = Field()

    @validator('nick_or_email')
    def make_nick_or_email(cls, v):
        return v.strip()

    @validator('user_agent')
    def make_user_agent(cls, v):
        return v.strip()


class UserCreateIn(BaseModel):
    nick: str = Field()
    email: EmailStr = Field()
    password: str = Field()
    code: str = Field()

    @validator('code')
    def make_code(cls, v):
        return v.strip()

    @validator('nick')
    def make_nick(cls, v):
        return v.strip()

    @validator('email')
    def make_email(cls, v):
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
    name: Optional[str] = Field(None)
    bio: Optional[str] = Field(None)

    @validator('bio')
    def make_bio(cls, v):
        return v.strip() if v else v

    @validator('name')
    def make_name(cls, v):
        return v.strip() if v else v


UserUpdateIn(name=None)


class IsEmailExistsOut(BaseModel):
    exists: bool = Field()


class IsNickExistsOut(BaseModel):
    exists: bool = Field()
