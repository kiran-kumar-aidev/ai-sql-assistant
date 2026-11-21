
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ecommerce.db"


def get_database_schema():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    # Retrieve all table names
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    schema_information = []

    for table in tables:

        table_name = table[0]

        # Retrieve column information
        cursor.execute(f"PRAGMA table_info({table_name})")

        columns = cursor.fetchall()

        column_names = [
            f"{column[1]} ({column[2]})"
            for column in columns
        ]

        schema_information.append(
            f"Table: {table_name}\n"
            f"Columns: {', '.join(column_names)}"
        )

        # Retrieve foreign key relationships
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")

        foreign_keys = cursor.fetchall()

        for fk in foreign_keys:

            relationship = (
                f"Relationship: {table_name}.{fk[3]} "
                f"references {fk[2]}.{fk[4]}"
            )

            schema_information.append(relationship)

    connection.close()

    return "\n\n".join(schema_information)


if __name__ == "__main__":

    schema = get_database_schema()

    print("DATABASE SCHEMA")
    print("================")
    print(schema)
