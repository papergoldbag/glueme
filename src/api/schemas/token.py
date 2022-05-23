from pydantic import Field, BaseModel


class TokenOut(BaseModel):
    id: int
    token: str
    user_agent: str

    class Config:
        orm_mode = True


class TokenDeviceOut(BaseModel):
    token_id: int = Field()
    user_agent: str = Field()
    is_me: bool = Field()

    class Config:
        orm_mode = True
