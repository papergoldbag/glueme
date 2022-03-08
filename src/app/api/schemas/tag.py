from datetime import datetime

from pydantic import BaseModel, Field


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
