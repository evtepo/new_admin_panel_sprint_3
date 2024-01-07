import psycopg2
from psycopg2.extensions import cursor as _cursor

import logging

from contextlib import contextmanager

from settings import dsl, pg_exceptions, elastic_exceptions, redis_exceptions
from extractor import (
    extract_pg_data, get_last_record,
    get_sub_record_id, get_query
)
from transformer import get_valid_data, get_modified_field
from state_redis import get_state
from loader import load_data
from etl_backoff import backoff


@contextmanager
def pg_connect(dsl: dict) -> _cursor:
    """
    Функция для подключения к PosgtreSQL
    """
    db = psycopg2.connect(**dsl)
    try:
        yield db.cursor()
    finally:
        db.close()


exceptions = pg_exceptions + elastic_exceptions + redis_exceptions


@backoff(exceptions=exceptions)
def run_movies_etl(dsl: dict) -> None:
    """
    Функция для запуска etl.
    """
    logging.log(
        logging.INFO,
        """
        ------------------------------------------------------------------------------
        - The script for transferring data from PostgreSQL to Elasticsearch started! -
        ------------------------------------------------------------------------------
        """
    )
    with pg_connect(dsl) as pg_conn:
        state = get_state()

        extract = extract_pg_data

        transform = get_valid_data
        get_modified = get_modified_field

        load = load_data
        index = "movies"

        film_work_key = "filmwork_modified"
        genre_key = "genre_modified"
        person_key = "person_modified"

        genre_table = "genre"
        person_table = "person"

        state.set_state(
            genre_key,
            str((get_last_record(pg_conn, genre_table)[-1]))
        )
        state.set_state(
            person_key,
            str((get_last_record(pg_conn, person_table)[-1]))
        )

        while True:
            genre_modified = state.get_state(genre_key)
            person_modified = state.get_state(person_key)

            genre = get_sub_record_id(pg_conn, genre_table, genre_modified)
            person = get_sub_record_id(pg_conn, person_table, person_modified)

            query = None
            if genre:
                query = get_query(pg_conn, genre_table, genre, genre_key, state)
            elif person:
                query = get_query(pg_conn, person_table, person, person_key, state)

            modified = state.get_state(film_work_key)
            if modified:
                data = extract(pg_conn, query, modified)
            else:
                data = extract(pg_conn, query)

            result = []

            for items in data:
                state.set_state(film_work_key, str(get_modified(*items[-1])))
                for item in items:
                    item = transform(*item)
                    result.append(item)

            load(result, index)


if __name__ == "__main__":
    run_movies_etl(dsl)
