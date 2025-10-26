# Django Blogging Platform

Includes basic CRUD operations for REST API built with Django.

## Requirements

- Python 3.13.7
- Django 5.2.7
- postgresql 17.5

## Installation

- Clone the repository
- Create and activate a virtual environment

``` shell
python3 -m venv .venv
source .venv/bin/activate
```

- Install the requirements

``` shell
pip install -r requirements.txt
```

- create user and database in postgresql

```shell
sudo -u postgres psql
```

```postgresql
CREATE USER <username> WITH ENCRYPTED PASSWORD '<password>';
CREATE DATABASE <dbname>;
GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username>;
\c <dbname>
GRANT ALL ON SCHEMA public TO <username>;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <username>;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO <username>;
\q
```

- Copy .env.example to .env and setup database credentials

```shell
cp .env.example .env
nano .env
```

- Run the server

```shell
python manage.py runserver
```

## Http Request File

There is a http request file in the docs directory with all methods and endpoints to manually test the API.

You'll need an http-client.private.env.json file in the docs directory with the following format:

```json
{
  "dev": {
    "url": "http://localhost:8000/",
    "id": "1"
  }
}
```
