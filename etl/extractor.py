from psycopg2.extensions import cursor as _cursor

from typing import Union, List, Tuple
from backoff import on_exception, expo

from settings import pg_exceptions


@on_exception(wait_gen=expo, exception=pg_exceptions, max_value=10)
def extract_pg_data(cursor: _cursor, limit: int = 100) -> List[Union[Tuple, None]]:
    """Функция для сбора данных из PostgreSQL"""

    cursor.execute(
        f"""
        SELECT  fw.id,
                fw.rating,
                array_agg(DISTINCT g.name) AS genre,
                fw.title,
                fw.description,
                COALESCE (
                    json_agg(
                        DISTINCT jsonb_build_object(
                            'person_role', pfw.role,
                            'person_id', p.id,
                            'person_name', p.full_name
                        )
                    ) FILTER (WHERE p.id is not null),
                    '[]'
                ) as persons
        FROM content.film_work fw
        LEFT OUTER JOIN content.genre_film_work gfw
            ON (fw.id = gfw.film_work_id)
        LEFT OUTER JOIN content.genre g
            ON (gfw.genre_id = g.id)
        LEFT OUTER JOIN content.person_film_work pfw
            ON (fw.id = pfw.film_work_id)
        LEFT OUTER JOIN content.person p
            ON (pfw.person_id = p.id)
        GROUP BY fw.id
        ORDER BY fw.modified
        """
    )

    while True:
        data = cursor.fetchmany(limit)
        if not data:
            break

        yield data
