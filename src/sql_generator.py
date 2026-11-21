
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()


# Pydantic model for structured SQL output
class SQLQueryOutput(BaseModel):
    sql_query: str = Field(
        description="A valid SQLite SELECT query"
    )


# Initialize Pydantic output parser
sql_parser = PydanticOutputParser(
    pydantic_object=SQLQueryOutput
)


# Initialize Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# SQL generation prompt
sql_prompt = ChatPromptTemplate.from_template(
    """
You are an expert SQLite SQL developer.

Your task is to convert the user's natural language question
into a valid SQLite SELECT query.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

IMPORTANT RULES:
1. Generate SQLite-compatible SQL.
2. Use only tables and columns present in the schema.
3. Use correct JOIN conditions based on foreign keys.
4. Generate only SELECT queries.
5. Never generate INSERT, UPDATE, DELETE, DROP or ALTER.
6. Do not invent table names or column names.
7. Return the output in the required structured format.
8. Do not include markdown code fences.

{format_instructions}
"""
)


def generate_sql(question, schema):

    messages = sql_prompt.format_messages(
        schema=schema,
        question=question,
        format_instructions=sql_parser.get_format_instructions()
    )

    response = llm.invoke(messages)

    # Parse and validate the LLM response using Pydantic
    parsed_output = sql_parser.parse(response.content)

    return parsed_output.sql_query.strip()


if __name__ == "__main__":

    from src.schema_inspector import get_database_schema

    schema = get_database_schema()

    question = "Show the top 5 customers by total purchase."

    generated_sql = generate_sql(question, schema)

    print("\nUSER QUESTION:")
    print(question)

    print("\nGENERATED SQL:")
    print(generated_sql)