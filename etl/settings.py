import os

import logging

from dotenv import load_dotenv

from psycopg2 import OperationalError, DatabaseError
from redis import ConnectionError
from elasticsearch import ConnectionError


load_dotenv()

ELASTIC_PORT = os.environ.get("ELASTIC_PORT")
ELASTIC_HOST = os.environ.get("ELASTIC_HOST")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

dsl = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT,
}

elastic_exceptions = (
    ConnectionError,
    DatabaseError,
)

redis_exceptions = (
    ConnectionError,
)

pg_exceptions = (
    OperationalError,
)

filename = logging.FileHandler("backoff_log.log")
console = logging.StreamHandler()

logging.basicConfig(
    handlers=(filename, console),
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)
