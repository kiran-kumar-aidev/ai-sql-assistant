
from unittest.mock import patch

from src.workflow_graph import run_sql_assistant


def test_workflow_rejects_unsafe_sql():

    unsafe_sql = "DELETE FROM customers"

    # Simulate the LLM generating unsafe SQL
    with patch(
        "src.graph_nodes.generate_sql",
        return_value=unsafe_sql
    ):

        # Execution must never be reached
        with patch(
            "src.graph_nodes.execute_sql"
        ) as mock_execute:

            result = run_sql_assistant(
                "Delete all customers"
            )

            print("\nGENERATED SQL:")
            print(result["generated_sql"])

            print("\nVALIDATION STATUS:")
            print(result["is_valid"])

            print("\nVALIDATION MESSAGE:")
            print(result["validation_message"])

            assert result["is_valid"] is False
            assert result["query_result"] is None

            mock_execute.assert_not_called()

            print("\nPASS: Unsafe SQL was blocked.")
            print("PASS: SQL execution was skipped.")


if __name__ == "__main__":
    test_workflow_rejects_unsafe_sql()
