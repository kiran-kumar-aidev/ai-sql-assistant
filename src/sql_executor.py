
import sqlite3
from pathlib import Path

from src.sql_validator import validate_sql


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ecommerce.db"


ALLOWED_TABLES = {
    "customers",
    "products",
    "orders",
    "order_items"
}


def sqlite_authorizer(action, arg1, arg2, database, trigger):

    # Allow only read operations on approved tables
    if action == sqlite3.SQLITE_SELECT:
        return sqlite3.SQLITE_OK

    if action == sqlite3.SQLITE_READ:

        if arg1 and arg1.lower() in ALLOWED_TABLES:
            return sqlite3.SQLITE_OK

        return sqlite3.SQLITE_DENY

    # Allow safe functions only
    if action == sqlite3.SQLITE_FUNCTION:

        function_name = (arg2 or arg1 or "").lower()

        if function_name in {
            "load_extension",
            "readfile",
            "writefile"
        }:
            return sqlite3.SQLITE_DENY

        return sqlite3.SQLITE_OK

    # Deny all other database operations
    return sqlite3.SQLITE_DENY


def execute_sql(sql_query):

    # Step 1: Validate SQL
    is_valid, message = validate_sql(sql_query)

    if not is_valid:
        raise ValueError(message)

    connection = None

    try:

        # Step 2: Open database in read-only mode
        connection = sqlite3.connect(
            f"{DB_PATH.resolve().as_uri()}?mode=ro",
            uri=True,
            timeout=5
        )

        # Step 3: Enable query-only mode
        connection.execute("PRAGMA query_only = ON")

        # Step 4: Register SQLite authorizer
        connection.set_authorizer(sqlite_authorizer)

        # Step 5: Set query execution limit
        connection.set_progress_handler(
            lambda: 1,
            1000000
        )

        # Step 6: Execute SQL
        cursor = connection.execute(sql_query)

        # Step 7: Retrieve column names
        columns = [
            description[0]
            for description in cursor.description
        ]

        # Step 8: Retrieve rows
        rows = cursor.fetchall()

        return {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }

    except sqlite3.Error as e:

        raise RuntimeError(
            f"Database execution failed: {e}"
        ) from e

    finally:

        if connection is not None:
            connection.close()


if __name__ == "__main__":

    query = """
    SELECT
        c.customer_name,
        SUM(oi.quantity * oi.unit_price) AS total_purchase
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_purchase DESC
    LIMIT 5
    """

    result = execute_sql(query)

    print("\nQUERY RESULTS:")

    for row in result["rows"]:
        print(row)

    print("\nTOTAL ROWS:", result["row_count"])
