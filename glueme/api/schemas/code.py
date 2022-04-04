from datetime import datetime

from pydantic import BaseModel, Field


class SentCodeOut(BaseModel):
    email: str
    created: datetime
    expired: datetime

    class Config:
        orm_mode = True


class CodeValidityOut(BaseModel):
    is_valid: bool = Field()
