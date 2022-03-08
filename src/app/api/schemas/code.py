from datetime import datetime

from pydantic import BaseModel, Field


class SentCodeOut(BaseModel):
    id: int = Field()
    code: str = Field()
    email: str = Field()
    created: datetime = Field()
    expired: datetime = Field()
    is_active: bool = Field()

    class Config:
        orm_mode = True


class CodeValidityOut(BaseModel):
    is_valid: bool = Field()
