import os
import pathlib

from pydantic import PostgresDsn, BaseSettings


class Settings(BaseSettings):
    database_url: PostgresDsn
    mailgun_domain: str
    mailgun_api_key: str
    max_sec_code_reg: int

    class Config:
        env_file = pathlib.Path(os.path.abspath(__file__)).parent.parent.parent / '.env'


settings: Settings = Settings()
