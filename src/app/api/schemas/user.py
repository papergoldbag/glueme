from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, EmailStr

from src.app.api.schemas.tag import TagOut


class UserAuth(BaseModel):
    nick_or_email: Union[str, EmailStr] = Field()
    password: str = Field()
    user_agent: str = Field()


class UserCreateIn(BaseModel):
    nick: str = Field()
    name: Optional[str] = Field(None)
    email: EmailStr = Field()
    password: str = Field()
    code: str = Field()


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
    nick: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    bio: Optional[str] = Field(None)


class IsEmailExistsOut(BaseModel):
    exists: bool = Field()


class IsNickExistsOut(BaseModel):
    exists: bool = Field()
