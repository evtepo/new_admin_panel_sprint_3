import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

from load_data import SQLiteExtractor
from transfer_data import PostgresSaver
from delete_data_from_sqlite import TransfomData

from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, SQLITE

from contextlib import contextmanager


@contextmanager
def sqlite_open_db(sqlite: str):
    conn = sqlite3.connect(sqlite)
    try:
        yield conn.cursor()
    finally:
        conn.commit()
        conn.close()


@contextmanager
def postgres_open_db(dsl: dict):
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try: 
        yield conn.cursor()
    finally:
        conn.commit()
        conn.close()


def load_from_sqlite(
        sqlite_cur: sqlite3.Connection.cursor,
        pg_cursor: psycopg2.connect,
        n: int = 10
):
    """Основной метод загрузки данных из SQLite в Postgres."""
    tables = (
        "film_work", "person_film_work",
        "genre", "person", "genre_film_work"
    )

    TransfomData(sqlite_cur).change_data()
    postgres_saver = PostgresSaver()
    sqlite_extractor = SQLiteExtractor(sqlite_cur)

    for table in tables:
        for data in sqlite_extractor.extract_movies(table, n):
            postgres_saver.save_all_data(table, data, pg_cursor, n)


if __name__ == "__main__":
    dsl = {
        "dbname": DB_NAME, "user": DB_USER,
        "password": DB_PASSWORD, "host": DB_HOST, "port": DB_PORT
    }
    with sqlite_open_db(SQLITE) as sqlite_cur, \
            postgres_open_db(dsl) as pg_cursor:
        load_from_sqlite(sqlite_cur, pg_cursor)
