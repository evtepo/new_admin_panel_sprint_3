from dataclasses import dataclass
from sqlite3 import Cursor


@dataclass(frozen=True)
class TransfomData:
    """
    Класс для подготовки таблиц к переносу.
    """
    connection: Cursor
    table: str = "film_work"

    def delete_wrong_data(self):
        """
        Функция для удаления лишних колонок.
        """
        cursor = self.connection
        new_table = "temporary_table"
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {new_table} AS
            SELECT id, title, description, creation_date, rating,
            type, created_at, updated_at
            FROM {self.table};
            """
        )
        cursor.execute(
            f"DROP TABLE IF EXISTS {self.table};"
        )
        cursor.execute(
            f"ALTER TABLE {new_table} RENAME TO {self.table};"
        )
