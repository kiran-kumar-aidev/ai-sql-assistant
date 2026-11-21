
from src.sql_generator import generate_sql
from src.sql_validator import validate_sql
from src.sql_executor import execute_sql
from src.sql_generator import llm


def generate_sql_node(state):

    print("Generating SQL...")

    try:
        sql_query = generate_sql(
            question=state["question"],
            schema=state["schema"]
        )

        return {
            "generated_sql": sql_query,
            "error": None
        }

    except Exception as e:
        return {
            "generated_sql": None,
            "error": f"SQL generation failed: {str(e)}"
        }


def validate_sql_node(state):

    print("Validating SQL...")

    sql_query = state.get("generated_sql")

    if not sql_query:
        return {
            "is_valid": False,
            "validation_message": "No SQL query was generated."
        }

    is_valid, message = validate_sql(sql_query)

    return {
        "is_valid": is_valid,
        "validation_message": message
    }


def execute_sql_node(state):

    print("Executing SQL...")

    try:
        result = execute_sql(
            state["generated_sql"]
        )

        return {
            "query_result": result,
            "error": None
        }

    except Exception as e:
        return {
            "query_result": None,
            "error": f"SQL execution failed: {str(e)}"
        }


def explain_result_node(state):

    print("Generating result explanation...")

    question = state["question"]
    sql_query = state["generated_sql"]
    result = state["query_result"]

    prompt = f"""
    You are a helpful data analyst.

    USER QUESTION:
    {question}

    EXECUTED SQL:
    {sql_query}

    QUERY RESULTS:
    Columns: {result['columns']}
    Rows: {result['rows']}
    Total Rows: {result['row_count']}

    Explain the results in simple English.

    Rules:
    1. Explain what the query found.
    2. Highlight important observations.
    3. Use actual values from the results.
    4. Do not invent facts.
    5. Keep the explanation concise.
    """

    response = llm.invoke(prompt)

    return {
        "explanation": response.content,
        "error": None
    }
