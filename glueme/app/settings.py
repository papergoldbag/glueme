import os
import pathlib

DATABASE_URL: str = 'postgresql://glueme_user:3455742@127.0.0.1:5432/glueme_db'
MAILGUN_DOMAIN: str = 'sandbox345705de53c1424599cbde573a5ffc51.mailgun.org'
MAILGUN_API_KEY: str = '6cdfcc06ab1ffec8e6cd1ac78600f809-e2e3d8ec-53fa5582'

DELAY_BETWEEN_REG_CODES: int = 30
LIFETIME_REG_CODE: int = 300

DELAY_BETWEEN_FORGOTPASS_CODES: int = 60
LIFETIME_FORGOTPASS_CODE: int = 300

LOG_PATH = pathlib.Path(os.path.abspath(__file__)).parent.parent.parent / '.env'


class CodeTypes:
    REG = 'reg'
    FORGOT_PASS = 'forgot_pass'


DEFAULT_TAGS = ['Бег', 'Прыжки', 'Машины', "Растения", 'Собаки', 'Компьютеры', 'Птицы']


def setup_from_env():
    global DATABASE_URL, MAILGUN_DOMAIN, MAILGUN_API_KEY, DELAY_BETWEEN_REG_CODES, DELAY_BETWEEN_FORGOTPASS_CODES, LIFETIME_FORGOTPASS_CODE, LIFETIME_REG_CODE
    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')

    DELAY_BETWEEN_REG_CODES = int(os.getenv('DELAY_BETWEEN_REG_CODES'))
    LIFETIME_REG_CODE = int(os.getenv('LIFETIME_REG_CODE'))

    DELAY_BETWEEN_FORGOTPASS_CODES = int(os.getenv('DELAY_BETWEEN_FORGOTPASS_CODES'))
    LIFETIME_FORGOTPASS_CODE = int(os.getenv('LIFETIME_FORGOTPASS_CODE'))
