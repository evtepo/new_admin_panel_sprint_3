import logging
import sqlite3
from dataclasses import dataclass


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
