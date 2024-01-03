import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

from typing import Union

from unittest import TestCase

from dataclasses import dataclass

from uuid import uuid4

from datetime import datetime

from settings import DB_NAME, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER, SQLITE


@dataclass
class UUIDMixin:
    id: uuid4


@dataclass
class Filmwork(UUIDMixin):
    title: str
    description: Union[str, None]
    creation_date: Union[datetime, None]
    rating: float
    type: str
    created: datetime
    modified: datetime

    def __post_init__(self):
        self.created = str(self.created)
        self.modified = str(self.modified)


@dataclass
class Person(UUIDMixin):
    full_name: str
    created: datetime
    modified: datetime

    def __post_init__(self):
        self.created = str(self.created)
        self.modified = str(self.modified)


@dataclass
class Genre(UUIDMixin):
    name: str
    description: Union[str, None]
    created: datetime
    modified: datetime

    def __post_init__(self):
        self.created = str(self.created)
        self.modified = str(self.modified)


@dataclass
class GenreFilmwork(UUIDMixin):
    genre_id: uuid4
    film_work_id: uuid4
    created: datetime

    def __post_init__(self):
        self.created = str(self.created)


@dataclass
class PersonFilmwork(UUIDMixin):
    film_work_id: uuid4
    person_id: uuid4
    role: str
    created: datetime

    def __post_init__(self):
        self.created = str(self.created)


dsl = {
    'dbname': DB_NAME, 'user': DB_USER,
    'password': DB_PASSWORD, 'host': DB_HOST, 'port': DB_PORT
}
with sqlite3.connect(SQLITE) as sq_conn, \
        psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:

    class TestTables(TestCase):
        sq_cur = sq_conn.cursor()
        pg_cursor = pg_conn.cursor()
        tables = (
            'person', 'film_work', 'genre',
            'person_film_work', 'genre_film_work'
        )
        dct_tables = {
            'person': Person,
            'film_work': Filmwork,
            'genre': Genre,
            'person_film_work': PersonFilmwork,
            'genre_film_work': GenreFilmwork,
        }

        def setUp(self):
            self.pg_data = {}
            self.sq_data = {}

            for table in self.tables:
                self.pg_cursor.execute(
                    f'SELECT * FROM content.{table};'
                )
                self.sq_cur.execute(
                    f'SELECT * FROM {table};'
                )
                pg_table_data = self.pg_cursor.fetchall()
                sq_table_data = self.sq_cur.fetchall()

                for items in pg_table_data:

                    self.pg_data.setdefault(table, []).append(
                        self.dct_tables[table](*items)
                    )

                for items in sq_table_data:
                    self.sq_data.setdefault(table, []).append(
                        self.dct_tables[table](*items)
                    )

        @classmethod
        def tearDownClass(cls):
            cls.sq_cur.close()
            cls.pg_cursor.close()

        def test_data_integrity(self):
            """
            Тест для проверки целостности данных.
            """
            for table in self.tables:
                self.assertEqual(
                    len(self.pg_data.get(table)), len(self.sq_data.get(table))
                )

        def data_similarity_check(self, table):
            """
            Функция для проверки схожести данных.
            """
            items_pg = self.pg_data.get(table)
            items_sq = self.pg_data.get(table)
            for i in range(len(items_pg)):
                for j in range(len(items_sq[i].__dict__.values())):
                    self.assertEqual(
                        tuple(items_pg[i].__dict__.values())[j],
                        tuple(items_sq[i].__dict__.values())[j]
                    )

        def test_film_work_data(self):
            self.data_similarity_check('film_work')

        def test_genre_data(self):
            self.data_similarity_check('genre')

        def test_person_data(self):
            self.data_similarity_check('person')

        def test_genre_film_work_data(self):
            self.data_similarity_check('genre_film_work')

        def test_person_film_work_data(self):
            self.data_similarity_check('person_film_work')
