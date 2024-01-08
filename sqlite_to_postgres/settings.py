import logging
import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    db_name: str = Field(alias="DB_NAME")
    db_user: str = Field(alias="DB_USER")
    db_password: str = Field(alias="DB_PASSWORD")
    db_host: str = Field(alias="DB_HOST")
    db_port: str = Field(alias="DB_PORT")

    sqlite = os.environ.get("SQLITE")


postgres_dsl: dict = {
    "dbname": Settings().db_name,
    "user": Settings().db_user,
    "password": Settings().db_password,
    "host": Settings().db_host,
    "port": Settings().db_port,
}

filename = logging.FileHandler("load_data_log.log")
console = logging.StreamHandler()

logging.basicConfig(
    handlers=(filename, console),
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)
