
from typing import TypedDict, Optional, Any


class SQLAssistantState(TypedDict):

    question: str

    schema: str

    generated_sql: Optional[str]

    is_valid: bool

    validation_message: Optional[str]

    query_result: Optional[dict[str, Any]]

    explanation: Optional[str]

    error: Optional[str]
