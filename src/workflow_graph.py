
from langgraph.graph import StateGraph, START, END

from src.graph_state import SQLAssistantState

from src.graph_nodes import (
    generate_sql_node,
    validate_sql_node,
    execute_sql_node,
    explain_result_node
)

from src.schema_inspector import get_database_schema


def route_after_generation(state):

    if state.get("error"):
        return "stop"

    return "validate"


def route_after_validation(state):

    if not state.get("is_valid"):
        return "stop"

    return "execute"


def route_after_execution(state):

    if state.get("error"):
        return "stop"

    return "explain"


def build_sql_workflow():

    workflow = StateGraph(SQLAssistantState)

    # Register nodes
    workflow.add_node(
        "generate_sql",
        generate_sql_node
    )

    workflow.add_node(
        "validate_sql",
        validate_sql_node
    )

    workflow.add_node(
        "execute_sql",
        execute_sql_node
    )

    workflow.add_node(
        "explain_result",
        explain_result_node
    )

    # Starting point
    workflow.add_edge(START, "generate_sql")

    # Conditional routing after SQL generation
    workflow.add_conditional_edges(
        "generate_sql",
        route_after_generation,
        {
            "validate": "validate_sql",
            "stop": END
        }
    )

    # Conditional routing after validation
    workflow.add_conditional_edges(
        "validate_sql",
        route_after_validation,
        {
            "execute": "execute_sql",
            "stop": END
        }
    )

    # Conditional routing after execution
    workflow.add_conditional_edges(
        "execute_sql",
        route_after_execution,
        {
            "explain": "explain_result",
            "stop": END
        }
    )

    workflow.add_edge(
        "explain_result",
        END
    )

    return workflow.compile()


def run_sql_assistant(question):

    schema = get_database_schema()

    app = build_sql_workflow()

    initial_state = {
        "question": question,
        "schema": schema,
        "generated_sql": None,
        "is_valid": False,
        "validation_message": None,
        "query_result": None,
        "explanation": None,
        "error": None
    }

    result = app.invoke(initial_state)

    return result
