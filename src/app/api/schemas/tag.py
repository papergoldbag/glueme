from datetime import datetime

from pydantic import BaseModel, Field, root_validator


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
    title: str = Field()

    @root_validator(pre=True)
    def check_values(cls, values):
        if not values:
            raise ValueError('no tag_id or title')
        return values
