from datetime import datetime

from pydantic import BaseModel, Field


class TagOut(BaseModel):
    id: int = Field()
    title: str = Field()
    created: datetime = Field()

    class Config:
        orm_mode = True


class AddTagIn(BaseModel):
    title: str = Field()

    class Config:
        orm_mode = True
