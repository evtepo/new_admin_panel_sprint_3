from psycopg2.extensions import cursor as _cursor


def extract_pg_data(
    cursor: _cursor, sub_query: str = None, modified: str = "", limit: int = 100
) -> list[tuple | None]:
    """Функция для сбора данных из PostgreSQL"""

    command = ""

    if modified:
        command = f"""WHERE fw.modified > timestamp '{modified}'"""
        if sub_query:
            command += f" OR fw.id IN ({sub_query})"

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
                ) as persons,
                fw.modified
        FROM content.film_work fw
        LEFT OUTER JOIN content.genre_film_work gfw
            ON (fw.id = gfw.film_work_id)
        LEFT OUTER JOIN content.genre g
            ON (gfw.genre_id = g.id)
        LEFT OUTER JOIN content.person_film_work pfw 
            ON (fw.id = pfw.film_work_id)
        LEFT OUTER JOIN content.person p
            ON (pfw.person_id = p.id)
        {command}
        GROUP BY fw.id
        ORDER BY fw.modified
        LIMIT {limit}
        """
    )

    while data := cursor.fetchmany(20):
        yield data


def get_last_record(cursor: _cursor, table_name: str) -> tuple:
    """Функция для получения записи с самым новым modified"""
    cursor.execute(
        f"""
        SELECT id, modified
        FROM content.{table_name}
        ORDER BY modified DESC
        LIMIT 1
        """
    )

    return cursor.fetchone()


def get_sub_record_id(cursor: _cursor, table_name: str, modified: str) -> str:
    """Функция для получения обновленной записи person или genre"""
    cursor.execute(
        f"""
        SELECT id, modified
        FROM content.{table_name}
        WHERE modified > timestamp '{modified}'
        """
    )

    t_id = cursor.fetchone()

    if t_id:
        return t_id


def get_sub_records(cursor: _cursor, table_name: str, t_id: str) -> list:
    """
    Функция для получения кинопроизведений,
    у которых были обновлены связанные модели
    """
    cursor.execute(
        f"""
        SELECT fw.id
        FROM content.film_work fw
        LEFT JOIN content.{table_name}_film_work tfw ON tfw.film_work_id = fw.id
        WHERE tfw.{table_name}_id = '{t_id}'
        """
    )

    result = cursor.fetchall()

    if result:
        return result


def get_query(pg_conn: _cursor, table_name: str, data: str, modified_field: str, state):
    """
    Функция для получения id film_work,
    у которых изменилось поле genre или person
    """
    state.set_state(modified_field, str(data[-1]))
    records = get_sub_records(pg_conn, str(table_name), f"{data[0]}")
    query = ", ".join(map(lambda x: f"'{x[0]}'", records))

    return query
