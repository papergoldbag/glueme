<a>GlueMe</a>
------------
<p>GlueMe - социальная сеть для мобильных устройств</p>
<p>Данный репозиторий - это api для работы клиентов</p>


СРЕДА ЗАПУСКА
------------
Развертывание сервиса производится на linux(ubuntu)


DEPLOY
------------

### Создание пользователя
~~~
sudo adduser glueme
sudo usermod -aG glueme
su - glueme
~~~

### install deps 
~~~
sudo apt update
sudo apt upgrade
sudo apt install postgresql postgresql-contrib
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10
curl -sSL https://install.python-poetry.org | python3 -
export PATH=$PATH:$HOME/.poetry/bin
~~~

### init db
~~~
sudo -i -u postgres
psql
~~~

### set .env file
~~~
DATABASE_URL = "postgresql://glueme_user:password@127.0.0.1/glueme_db"
MAILGUN_DOMAIN = "domain"
MAILGUN_API_KEY = "api_key"
MAX_SEC_CODE_REG = 300
~~~

### init rep
~~~
git clone git@github.com:papergoldbag/glueme.git
poetry install
~~~

