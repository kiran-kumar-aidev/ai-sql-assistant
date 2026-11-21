
import sqlite3

from src.sql_executor import execute_sql


def test_database_security():

    unsafe_queries = [
        "DELETE FROM customers",
        "UPDATE customers SET city = 'Delhi'",
        "INSERT INTO customers VALUES (99, 'Test', 'test@test.com', 'Delhi')",
        "DROP TABLE customers"
    ]

    for query in unsafe_queries:

        print("\nTesting:", query)

        try:
            execute_sql(query)

            raise AssertionError(
                "Unsafe query was unexpectedly executed!"
            )

        except (ValueError, RuntimeError) as e:

            print("BLOCKED:", e)

    # Verify original database records remain unchanged
    connection = sqlite3.connect(
        "file:data/ecommerce.db?mode=ro",
        uri=True
    )

    customer_count = connection.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    connection.close()

    print("\nCustomer records:", customer_count)

    assert customer_count == 6

    print("\nAll database security tests passed!")


if __name__ == "__main__":
    test_database_security()
