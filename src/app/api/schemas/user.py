from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, EmailStr


class TagOut(BaseModel):
    id: int = Field()
    tag: str = Field()
    created: datetime = Field()

    class Config:
        orm_mode = True


class AddTagIn(BaseModel):
    tag: str = Field()

    class Config:
        orm_mode = True


class TokenOut(BaseModel):
    id: int = Field()
    token: str = Field()
    user_agent: str = Field()
    user_id: int = Field()

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    nick_or_email: Union[str, EmailStr] = Field()
    password: str = Field()
    user_agent: str = Field()


class CreateUserIn(BaseModel):
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


class IsEmailExistsOut(BaseModel):
    exists: bool = Field()


class IsNickExistsOut(BaseModel):
    exists: bool = Field()
