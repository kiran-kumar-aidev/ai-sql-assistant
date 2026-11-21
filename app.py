
import streamlit as st
import pandas as pd

from src.database import initialize_database
from src.workflow_graph import run_sql_assistant


# --------------------------------------------------
# Initialize database once when the app starts
# --------------------------------------------------

@st.cache_resource
def setup_database():
    initialize_database()


setup_database()


# --------------------------------------------------
# Streamlit page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI SQL Assistant")

st.caption(
    "Convert natural language into SQL, "
    "execute queries safely, and understand the results."
)

st.divider()


# --------------------------------------------------
# User input
# --------------------------------------------------

st.subheader("Ask your database")

question = st.text_area(
    "Enter your question in plain English",
    placeholder="Example: Show the top 5 customers by total purchase.",
    height=100
)

analyze_button = st.button(
    "Generate SQL & Execute",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# Execute AI SQL workflow
# --------------------------------------------------

if analyze_button:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Processing your question..."):

            try:
                result = run_sql_assistant(question)

                st.session_state["sql_result"] = result

            except Exception as e:

                st.error(f"Workflow failed: {e}")


# --------------------------------------------------
# Display results
# --------------------------------------------------

if "sql_result" in st.session_state:

    result = st.session_state["sql_result"]

    st.divider()

    # Generated SQL
    st.subheader("1. Generated SQL")

    generated_sql = result.get("generated_sql")

    if generated_sql:
        st.code(generated_sql, language="sql")
    else:
        st.info("SQL generation was unsuccessful.")

    # SQL Validation
    st.subheader("2. SQL Validation")

    if result.get("is_valid"):
        st.success(result.get("validation_message"))
    else:
        st.error(
            result.get("validation_message")
            or result.get("error")
            or "SQL validation failed."
        )

    # Stop displaying results if workflow failed
    if result.get("error"):

        st.error(result["error"])

    elif result.get("is_valid") and result.get("query_result"):

        query_result = result["query_result"]

        st.divider()

        # Query Results
        st.subheader("3. Query Results")

        df = pd.DataFrame(
            query_result["rows"],
            columns=query_result["columns"]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total records returned: {query_result['row_count']}"
        )

        # CSV Download
        st.download_button(
            "Download Results as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="sql_query_results.csv",
            mime="text/csv"
        )

        st.divider()

        # AI Explanation
        st.subheader("4. AI Result Explanation")

        explanation = result.get("explanation")

        if explanation:
            st.markdown(explanation)
        else:
            st.info("No explanation was generated.")

    elif result.get("is_valid"):

        st.info("The query completed without returning result data.")
