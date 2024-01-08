import logging

from dotenv import load_dotenv
from elasticsearch import ConnectionError as EsConnectionError
from psycopg2 import DatabaseError, OperationalError
from pydantic import Field
from pydantic_settings import BaseSettings
from redis import ConnectionError as RedisConnectionError

load_dotenv()


class Settings(BaseSettings):
    elastic_http: str = Field(alias="ELASTIC_HTTP")
    elastic_host: str = Field(alias="ELASTIC_HOST")
    elastic_port: str = Field(alias="ELASTIC_PORT")

    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: str = Field(alias="REDIS_PORT")

    db_name: str = Field(alias="DB_NAME")
    db_user: str = Field(alias="DB_USER")
    db_password: str = Field(alias="DB_PASSWORD")
    db_host: str = Field(alias="DB_HOST")
    db_port: str = Field(alias="DB_PORT")

    elastic_exceptions: tuple = (
        EsConnectionError,
        DatabaseError,
    )

    redis_exceptions: tuple = (RedisConnectionError,)

    pg_exceptions: tuple = (OperationalError,)


filename = logging.FileHandler("backoff_log.log")
console = logging.StreamHandler()

logging.basicConfig(
    handlers=(filename, console),
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)
