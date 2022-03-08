import os
import pathlib

from pydantic import PostgresDsn, BaseSettings


class Settings(BaseSettings):
    database_url: PostgresDsn
    mailgun_domain: str
    mailgun_api_key: str
    max_sec_code_reg: int

    class Config:
        _env_file = pathlib.Path(os.path.abspath(__file__)).parent.parent.parent / '.env'
        if os.path.exists(_env_file):
            env_file = _env_file


settings: Settings = Settings()
