
from src.workflow_graph import run_sql_assistant


def test_sql_assistant():

    question = "Show the top 5 customers by total purchase."

    print("\nUSER QUESTION:")
    print(question)

    result = run_sql_assistant(question)

    print("\n" + "=" * 50)
    print("GENERATED SQL")
    print("=" * 50)
    print(result.get("generated_sql"))

    print("\nVALIDATION STATUS:")
    print(result.get("is_valid"))

    print("\nVALIDATION MESSAGE:")
    print(result.get("validation_message"))

    if result.get("error"):
        print("\nERROR:")
        print(result["error"])
        return

    print("\nQUERY RESULTS:")
    print(result.get("query_result"))

    print("\nAI EXPLANATION:")
    print(result.get("explanation"))


if __name__ == "__main__":
    test_sql_assistant()
