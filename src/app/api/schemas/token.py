from pydantic import Field, BaseModel


class TokenOut(BaseModel):
    id: int = Field()
    token: str = Field()
    user_agent: str = Field()
    user_id: int = Field()

    class Config:
        orm_mode = True


class TokenDevicesOut(BaseModel):
    id: int = Field()
    user_agent: str = Field()
    is_me: bool = Field()

    class Config:
        orm_mode = True
