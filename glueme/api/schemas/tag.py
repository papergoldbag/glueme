from datetime import datetime

from pydantic import BaseModel, Field


class TagOut(BaseModel):
    id: int
    title: str
    created: datetime

    class Config:
        orm_mode = True


class TagWithIsMyOut(TagOut):
    is_my: bool = Field()


class AddTagWithIdIn(BaseModel):
    tag_id: int = Field()


class AddTagWithTitleIn(BaseModel):
    title: str = Field(min_length=2)
