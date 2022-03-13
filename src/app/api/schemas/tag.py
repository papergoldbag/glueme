from datetime import datetime

from pydantic import BaseModel, Field


class TagOut(BaseModel):
    id: int = Field()
    title: str = Field()
    created: datetime = Field()

    class Config:
        orm_mode = True


class TagWithIsMyOut(TagOut):
    is_my: bool = Field()


class AddTagWithIdIn(BaseModel):
    tag_id: int = Field()


class AddTagWithTitleIn(BaseModel):
    title: str = Field(min_length=2)
