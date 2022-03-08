from datetime import datetime

from pydantic import BaseModel, Field


class SentCode(BaseModel):
    id: int = Field()
    code: str = Field()
    email: str = Field()
    created: datetime = Field()
    expired: datetime = Field()
    is_active: bool = Field()

    class Config:
        orm_mode = True


class CodeWasSent(BaseModel):
    is_sent: bool = Field()
    sent_code: SentCode = Field()


class CodeValidity(BaseModel):
    is_valid: bool = Field()
