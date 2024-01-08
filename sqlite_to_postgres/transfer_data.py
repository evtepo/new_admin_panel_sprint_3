from dataclasses import dataclass


@dataclass
class PostgresSaver:
    """
    Класс для записи данных с sqlite3 в PostgreSQL.
    """

    columns = {
        "film_work": (
            "id",
            "title",
            "description",
            "creation_date",
            "rating",
            "type",
            "created",
            "modified",
        ),
        "genre": ("id", "name", "description", "created", "modified"),
        "person": ("id", "full_name", "created", "modified"),
        "person_film_work": ("id", "film_work_id", "person_id", "role", "created"),
        "genre_film_work": ("id", "film_work_id", "genre_id", "created"),
    }
    args = {
        "film_work": "(%s, %s, %s, %s, %s, %s, %s, %s)",
        "genre": "(%s, %s, %s, %s, %s)",
        "person": "(%s, %s, %s, %s)",
        "person_film_work": "(%s, %s, %s, %s, %s)",
        "genre_film_work": "(%s, %s, %s, %s)",
    }

    def save_all_data(self, table, data, cursor, n):
        """
        Функция перебора данных.
        """
        amount_of_data = 0
        cnt = 0
        records = list()
        while amount_of_data < len(data):
            if cnt == n:
                records.append(tuple(data[amount_of_data]))
                self.insert_data_by_table_name(table, cursor, records)
                records = list()
                cnt = 0
            else:
                records.append(tuple(data[amount_of_data]))
                cnt += 1
            amount_of_data += 1
        else:
            if cnt:
                self.insert_data_by_table_name(table, cursor, records)

    def insert_data_by_table_name(self, table, cursor, data):
        """
        Функия подготовки данных к вставке.
        """
        column = ",".join(self.columns.get(table))
        args = ",".join(cursor.mogrify(self.args[table], item).decode() for item in data)
        self.transfer_execution(cursor, args, table, column)

    def transfer_execution(self, cursor, args, table_name, items):
        """
        Функция для вставки данных.
        """
        cursor.execute(
            f"""
            INSERT INTO content.{table_name} ({items})
            VALUES {args}
            ON CONFLICT (id) DO NOTHING;
            """
        )
