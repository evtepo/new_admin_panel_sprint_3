import psycopg2
from psycopg2.extensions import cursor as _cursor

from backoff import on_exception, expo

from contextlib import contextmanager

from settings import dsl, pg_exceptions
from extractor import extract_pg_data
from transformer import get_valid_data
from state_redis import get_state
from loader import load_data


@contextmanager
@on_exception(wait_gen=expo, exception=pg_exceptions, max_value=10)
def pg_connect(dsl: dict) -> _cursor:
    db = psycopg2.connect(**dsl)
    try:
        yield db.cursor()
    finally:
        db.close()


def run_movies_etl(dsl: dict):
    with pg_connect(dsl) as pg_conn:
        state = get_state()

        extract = extract_pg_data

        transform = get_valid_data

        load = load_data
        index = "movies"

        for items in extract(pg_conn):
            for item in items:
                item = transform(*item)
                if state.get_state(item.get("id")) != item:
                    state.set_state(item.get("id"), item)
                    load(item, index)                   


if __name__ == "__main__":
    run_movies_etl(dsl)
