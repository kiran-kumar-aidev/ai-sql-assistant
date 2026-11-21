
import sqlglot
from sqlglot import exp


ALLOWED_TABLES = {
    "customers",
    "products",
    "orders",
    "order_items"
}

BLOCKED_FUNCTIONS = {
    "load_extension",
    "readfile",
    "writefile",
    "edit"
}


def validate_sql(sql_query):

    try:
        # Basic input validation
        if not isinstance(sql_query, str) or not sql_query.strip():
            return False, "SQL query cannot be empty."

        if len(sql_query) > 10000:
            return False, "SQL query exceeds the allowed length."

        # Parse SQL using SQLite dialect
        statements = sqlglot.parse(
            sql_query,
            read="sqlite"
        )

        # Reject empty or multiple statements
        if not statements or len(statements) != 1:
            return False, "Only one SQL statement is allowed."

        parsed_query = statements[0]

        if parsed_query is None:
            return False, "Invalid SQL query."

        # Allow only SELECT statements
        if not isinstance(parsed_query, exp.Select):
            return False, "Only SELECT queries are allowed."

        # Reject SELECT INTO
        if any(parsed_query.find_all(exp.Into)):
            return False, "SELECT INTO operations are not allowed."

        # Reject CTEs for the initial implementation
        if any(parsed_query.find_all(exp.With)):
            return False, "CTE queries are not currently allowed."

        # Check referenced tables
        referenced_tables = set()

        for table in parsed_query.find_all(exp.Table):

            # Reject table-valued functions
            if not isinstance(table.this, exp.Identifier):
                return False, "Table-valued functions are not allowed."

            # Reject database/schema-qualified table references
            if table.db or table.catalog:
                return False, "Qualified table references are not allowed."

            table_name = table.name.lower()

            referenced_tables.add(table_name)

        invalid_tables = referenced_tables - ALLOWED_TABLES

        if invalid_tables:
            return False, (
                "Access to unauthorized tables: "
                f"{', '.join(sorted(invalid_tables))}"
            )

        # Check potentially dangerous SQL functions
        for function in parsed_query.find_all(exp.Anonymous):

            function_name = function.name.lower()

            if function_name in BLOCKED_FUNCTIONS:
                return False, (
                    f"SQL function '{function_name}' "
                    "is not allowed."
                )

        return True, "SQL query validated successfully."

    except sqlglot.errors.ParseError:
        return False, "Invalid SQL syntax."

    except Exception:
        return False, "SQL validation failed."


if __name__ == "__main__":

    test_queries = [
        "SELECT * FROM customers",

        "SELECT COUNT(*) FROM orders",

        "SELECT * FROM customers; DROP TABLE orders",

        "DELETE FROM customers",

        "SELECT * FROM secret_table",

        "SELECT load_extension('test')",

        "SELECT readfile('/etc/passwd')",

        "WITH temp AS (SELECT * FROM customers) SELECT * FROM temp"
    ]

    for query in test_queries:

        is_valid, message = validate_sql(query)

        print("\nSQL:", query)
        print("VALID:", is_valid)
        print("MESSAGE:", message)
