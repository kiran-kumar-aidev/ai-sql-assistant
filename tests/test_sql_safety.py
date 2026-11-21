
from src.sql_validator import validate_sql


def test_sql_safety():

    test_cases = [
        ("SELECT * FROM customers", True),
        ("SELECT COUNT(*) FROM orders", True),
        ("DELETE FROM customers", False),
        ("DROP TABLE customers", False),
        ("UPDATE customers SET city='Delhi'", False),
        ("INSERT INTO customers VALUES (7,'Test','test@test.com','Delhi')", False),
        ("SELECT * FROM customers; DROP TABLE orders", False),
        ("SELECT * FROM secret_table", False)
    ]

    for query, expected in test_cases:

        is_valid, message = validate_sql(query)

        status = "PASS" if is_valid == expected else "FAIL"

        print(f"\n[{status}] {query}")
        print("Result:", message)

        assert is_valid == expected, (
            f"Unexpected validation result for: {query}"
        )


if __name__ == "__main__":
    test_sql_safety()
    print("\nAll SQL safety tests passed!")
