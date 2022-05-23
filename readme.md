<a>GlueMe</a>
------------
<p>GlueMe - социальная сеть для мобильных устройств</p>
<p>Это стартовая версия проекта, поэтому код не супер разделен на MVC</p>
<p>Не использовал Docker, в будущем можно подрубить</p>
<p>Также для старта юзал Sqlalchemy, потом можно на async databases перейти</p>
<p>Еще надо бы глобальный error handler добавить</p>


СРЕДА ЗАПУСКА
------------
Развертывание сервиса производится на linux(ubuntu20)


DEPLOY
------------

### Install and Update
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

### Настройка базы данных
~~~
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

### Установка Poetry
~~~
su - glueme
curl -sSL https://install.python-poetry.org | python3.10 -
export PATH=$PATH:$HOME/.poetry/bin
poetry config virtualenvs.in-project true
~~~

### Работа с Репозиторием
~~~
su - glueme
git clone git@github.com:papergoldbag/glueme.git
cd glueme
poetry env use python3.10
poetry install
~~~

### Пример Файла настроек src/glueme/settings.py
~~~
import os
import pathlib


TITLE = 'Glue Me API'

APIKEY: str = 'apikey'
API_PREFIX = '/api'

DATABASE_URL: str = 'postgresql://glueme:3455742@{server_ip}:5432/glueme'

MAILRU_LOGIN: str = 'support@gluemeproject.ru'
MAILRU_PASS: str = 'Support123456789'
MAILRU_SERVER: str = 'smtp.mail.ru'
MAILRU_PORT: int = 465

DELAY_BETWEEN_REG_CODES: int = 30
LIFETIME_REG_CODE: int = 300

DELAY_BETWEEN_FORGOTPASS_CODES: int = 60
LIFETIME_FORGOTPASS_CODE: int = 300

LOG_PATH: str = str(pathlib.Path(os.path.abspath(__file__)).parent.parent.parent / 'story.log')

DEFAULT_TAGS: list[str] = ['Бег', 'Прыжки', 'Машины', "Растения", 'Собаки', 'Компьютеры', 'Птицы']
~~~


### Создаём сервис glueme
~~~
sudo cp /home/glueme/glueme/deploy/glueme.service /etc/systemd/glueme.service
sudo systemctl start glueme.service
~~~

### Проверем статус сервиса
~~~
sudo systemctl status glueme.service
~~~

### Настройка NGINX
~~~
sudo cp /home/glueme/glueme/deploy/gluemenginx.txt /etc/nginx/sites-enabled/glueme
sudo sudo systemctl restart nginx
~~~


### Настройка сертификатов
~~~
sudo certbot certonly --nginx
...
~~~