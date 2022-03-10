from datetime import datetime

from pydantic import BaseModel, Field, root_validator


class TagOut(BaseModel):
    id: int = Field()
    title: str = Field()
    created: datetime = Field()

    class Config:
        orm_mode = True


class AddTagWithIdIn(BaseModel):
    tag_id: int = Field(None)


class AddTagWithTitleIn(BaseModel):
    title: str = Field(None)

    @root_validator
    def validate(cls, v):
        if not v:
            raise ValueError('no tag_id or title')

    class Config:
        orm_mode = True
