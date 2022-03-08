from datetime import datetime

from pydantic import BaseModel, Field


class SentCodeStatusOut(BaseModel):
    is_sent: bool = Field()

    class Config:
        orm_mode = True


class CodeValidityOut(BaseModel):
    is_valid: bool = Field()
