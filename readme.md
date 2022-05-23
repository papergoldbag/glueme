<a>GlueMe</a>
------------
<p>GlueMe - социальная сеть для мобильных устройств</p>


СРЕДА ЗАПУСКА
------------
Развертывание сервиса производится на linux(ubuntu20)
Поскольку это стартовая версия, то использовал монолит в коде
Также не использовал Docker, на данном этапе это не нужно


DEPLOY
------------

### Зависимости
~~~
sudo apt update
sudo apt upgrade
sudo apt install postgresql postgresql-contrib
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10
sudo apt install python3.10-venv
sudo apt install nginx
sudo apt install snapd
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
~~~

### База данных
~~~
sudo systemctl start postgresql
sudo -i -u postgres
psql
create user glueme with password 'PASSWORD' CREATEDB;
create database glueme with owner glueme encoding 'UTF8';
~~~

### Создание пользователя
~~~
sudo adduser glueme
sudo usermod -aG glueme
~~~

### Репозиторий
~~~
su - glueme

curl -sSL https://install.python-poetry.org | python3.10 -
export PATH=$PATH:$HOME/.poetry/bin
poetry config virtualenvs.in-project true

git clone git@github.com:papergoldbag/glueme.git
cd glueme
poetry env use python3.10
poetry install
~~~

### Файл настроек ./glueme/app/settings.py
~~~
import os
import pathlib

APIKEY: str = 'apikey'
DATABASE_URL: str = ...
MAILRU_LOGIN: str = ...
MAILRU_PASS: str = ...

DELAY_BETWEEN_REG_CODES: int = 30
LIFETIME_REG_CODE: int = 300

DELAY_BETWEEN_FORGOTPASS_CODES: int = 60
LIFETIME_FORGOTPASS_CODE: int = 300

LOG_PATH: str = str(pathlib.Path(os.path.abspath(__file__)).parent.parent.parent / '.env')


class CodeTypes:
    REG: str = 'reg'
    FORGOT_PASS: str = 'forgot_pass'


DEFAULT_TAGS: list[str] = ['Бег', 'Прыжки', 'Машины', "Растения", 'Собаки', 'Компьютеры', 'Птицы']
~~~
