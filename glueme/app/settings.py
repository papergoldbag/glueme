DATABASE_URL: str = 'postgresql://glueme_user:3455742@127.0.0.1:5432/glueme_db'
MAILGUN_DOMAIN: str = 'sandbox345705de53c1424599cbde573a5ffc51.mailgun.org'
MAILGUN_API_KEY: str = '6cdfcc06ab1ffec8e6cd1ac78600f809-e2e3d8ec-53fa5582'
DELAY_BETWEEN_REG_CODES: int = 30
LIFETIME_REG_CODE: int = 300


class CodeTypes:
    REG = 'reg'


DEFAULT_TAGS = ['Бег', 'Прыжки', 'Машины', "Растения", 'Собаки', 'Компьютеры', 'Птицы']
