from typing import Union

from pydantic import BaseModel, EmailStr, validator


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
