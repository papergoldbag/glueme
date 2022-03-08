import os
import pathlib

from pydantic import PostgresDsn, BaseSettings, validator


class Settings(BaseSettings):
    database_url: PostgresDsn
    mailgun_domain: str
    mailgun_api_key: str
    max_sec_code_reg: int

    @validator('database_url')
    def change_postgresql_url(cls, v: str):
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql://", 1)
        return v

    class Config:
        env_file = pathlib.Path(os.path.abspath(__file__)).parent.parent.parent / '.env'


settings: Settings = Settings()
