from dataclasses import dataclass

import sqlite3

import logging


filename = logging.FileHandler("load_data_log.log")
console = logging.StreamHandler()


logging.basicConfig(
    handlers=(filename, console),
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s"
)


@dataclass
class SQLiteExtractor:
    """
    Класс для загрузки данных из sqlite3
    """
    connection: sqlite3.Connection.cursor

    def extract_movies(self, table, n):
        cur = self.connection
        try:
            if table == "film_work":
                cur.execute(
                    f"SELECT id, title, description, creation_date, \
                    rating, type, created_at, updated_at FROM {table};"
                )
            else:
                cur.execute(f"SELECT * FROM {table};")
        except Exception as ex:
            logging.error(f"{ex}")

        while True:
            data = cur.fetchmany(n)
            if not data:
                break

            yield data
