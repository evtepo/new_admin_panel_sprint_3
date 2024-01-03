from dataclasses import dataclass

import sqlite3


@dataclass(frozen=True)
class TransfomData:
    """
    Класс для подготовки таблиц к переносу.
    """
    connection: sqlite3.Connection.cursor
    tables: tuple = (
        "film_work", "person_film_work",
        "genre", "person", "genre_film_work"
    )
    names = {
        "person_film_work": "film_work_id, person_id, role",
        "genre_film_work": "film_work_id, genre_id",
        "person": "full_name",
        "genre": "name",
        "film_work": "title",
    }

    def change_data(self):
        """
        Функция для удаления дубликатов.
        """
        cursor = self.connection

        for table in self.tables:
            if table == "film_work":
                self.delete_wrong_data(cursor, table)

            name = self.names.get(table)
            cursor.execute(
                f"""
                DELETE FROM {table}
                WHERE ROWID NOT IN (SELECT MIN(ROWID)
                FROM {table}
                GROUP BY {name});
                """
            )

    def delete_wrong_data(self, cursor, table):
        """
        Функция для удаления лишних колонок.
        """
        new_table = "temporary_table"
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {new_table} AS
            SELECT id, title, description, creation_date, rating,
            type, created_at, updated_at
            FROM {table};
            """
        )
        cursor.execute(
            f"DROP TABLE IF EXISTS {table};"
        )
        cursor.execute(
            f"ALTER TABLE {new_table} RENAME TO {table};"
        )
