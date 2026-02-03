import streamlit as st
import sqlite3
import pandas as pd
import os
import re
import json
from dotenv import load_dotenv
from query_llm import LLMQueryHandler
from system_prompt import sys_prompt
load_dotenv()

VECTOR_STORE = os.environ.get("VECTOR_STORE")
EMBED_MODEL = os.environ.get("EMBED_MODEL")
GPT_MODEL = os.environ.get("GPT_MODEL")
METRIC_FILENAME = os.environ.get("METRIC_FILENAME")
CONTEXT_PROMPT_FILE_PATH = os.environ.get("CONTEXT_PROMPT_FILE_PATH")
DB_PATH = os.environ.get("DB_PATH", "patient_health_data.db")

def get_column_names_from_db(db_path: str, sql_query: str) -> list[str]:
    """
    Retrieves the column names from a SQL query execution result.

    This function connects to a SQLite database, executes a provided SQL query,
    and extracts the column names from the query result.

    Parameters:
    ----
    - db_path (str): The file path to the SQLite database.
    - sql_query (str): The SQL query to execute for which the column names are needed.

    Returns:
    ----
    - list[str]: A list of column names (str) from the SQL query result.
    """
    cols = []
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        data = cursor.execute(sql_query)
        n_cols = len(data.description)
        for i in range(n_cols):
            cols.append(data.description[i][0])

    return cols


def execute_sql_on_db(db_path: str, query: str, params=None) -> tuple[pd.DataFrame | None, str | None]:
    """
    Executes SQL query on specified SQLite3 database and returns a tuple (DataFrame, error).

    Parameters:
    ----
    - db_path (str): The file path to the SQLite database.
    - query (str): The SQL query to execute.
    - params (dict, optional): Parameters to bind to the query.

    Returns:
    ----
    - (pandas.DataFrame | None, str | None): Tuple where the first element is the query result
      DataFrame when successful, otherwise None; the second element is an error message when
      execution failed, otherwise None.
    """
    with sqlite3.connect(db_path) as connection:
        try:
            df = pd.read_sql_query(query, connection, params)
            return df, None
        except Exception as e:
            # Return the error message so the caller (UI / CLI) can parse and display it
            return None, str(e)
             
def display_schemas(schemas):
    st.markdown("## Semantically Similar Schemas")
    len_sc = len(schemas)
    st.text(len_sc)
    for schema in schemas:
        # Support multiple schema formats safely
        description = ""
        sql_statement = schema

        # Format 1: '...Schema:\n<SQL>'
        if "Schema:\n" in schema:
            parts = schema.split("Schema:\n", 1)
            description = parts[0].strip()
            sql_statement = parts[1].strip()
        else:
            # Format 2: try to locate the first CREATE TABLE and split there
            m = re.search(r"(CREATE TABLE[\s\S]*)", schema, re.IGNORECASE)
            if m:
                sql_statement = m.group(1).strip()
                description = schema[: m.start(1)].strip()
            else:
                # Fallback: treat entire text as description if no SQL found
                description = schema.strip()

        match = re.search(r"CREATE TABLE\s+([^\s(]+)", sql_statement, re.IGNORECASE)
        if match:
            st.markdown(f"### {match.group(1)}")

        if description:
            st.markdown(description)

        # Ensure we always display something even if SQL is missing
        st.code(sql_statement or "(no SQL available)", language="sql")


def reset_app():
    keys_to_reset = ["user_has_interacted", "context_prompt", "user_prompt"]
    for key in keys_to_reset:
        st.session_state[key] = "" if key == "user_prompt" else None


def update_query_cost(new_cost):
    data = read_metric_file()
    if data["total_cost"] is None:
        data["total_cost"] = 0.0
    data["total_cost"] += new_cost
    with open(METRIC_FILENAME, "w") as f:
        json.dump(data, f)


def get_visitor_count():
    with open(METRIC_FILENAME, "r") as f:
        data = json.load(f)
        return data["visitor_count"]


def increment_visitor_count():
    data = read_metric_file()
    data["visitor_count"] += 1
    with open(METRIC_FILENAME, "w") as f:
        json.dump(data, f)


def read_metric_file():
    if not os.path.exists(METRIC_FILENAME):
        with open(METRIC_FILENAME, "w") as f:
            data = {"total_cost": 0.0, "visitor_count": 0}
            json.dump(data, f)
        return data
    else:
        with open(METRIC_FILENAME, "r") as f:
            data = json.load(f)
        return data

# try:
#     with open(CONTEXT_PROMPT_FILE_PATH) as f:
#         default_context_prompt = f.read()
# except Exception:
#     default_context_prompt = ""

# increment_visitor_count()
# visitor_count = get_visitor_count()
# st.sidebar.write(f"Visitor Count: {visitor_count}")

# user_prompt = st.text_input("User Prompt:", key="user_prompt")
# st.write(f"Your prompt is: {user_prompt}")
# user_has_interacted = True


# ask_for_context_prompt = st.radio(
#     "Do you want to enter a context prompt?",
#     ["Yes", "No"],
#     index=1,
#     key="ask_for_context_prompt",
# )
# if ask_for_context_prompt == "Yes" or default_context_prompt:
#     context_prompt = st.text_input("Context prompt:", key="context_prompt")
#     if not context_prompt:
#         st.warning("Please enter the context prompt to proceed.")
#         st.stop()
# else:
#     context_prompt = default_context_prompt

# view_context = st.checkbox("View Context Prompt")
# if view_context:
#     st.write(context_prompt)

# if user_prompt and user_has_interacted:
#     with st.spinner("Processing..."):

#         try:
#             handler = LLMQueryHandler(
#                 model=GPT_MODEL,
#                 vector_store=VECTOR_STORE,
#                 embed_model=EMBED_MODEL,
#                 db_path=DB_PATH,
#                 top_k=3,
#             )

#             schemas = handler.get_semantic_schemas(user_prompt)

#             display_schemas(schemas)
#             system_prompt = sys_prompt.format(schemas="\n\n".join(schemas), context=context_prompt)
            
#             st.markdown("Generated SQL Query and Results")
#             # Process the user query (handles initial prompt, retries, and SQL execution)
#             df, output = handler.process_user_query(schemas, user_prompt, context_prompt, system_prompt)

#             if output is None:
#                 st.error("LLM failed to generate a valid SQL query after retries.")
#             else:
#                 sql_query = output.get("SQL_QUERY")
#                 st.write("SQL Query:")
#                 st.code(sql_query, language="sql")

#                 # calculate_query_execution_cost expects (n_prompt_tokens, n_generated_tokens)
#                 cost = handler.calculate_query_execution_cost(
#                     output.get("N_PROMPT_TOKENS", 0), output.get("N_GENERATED_TOKENS", 0)
#                 )
#                 update_query_cost(cost)
#                 data = read_metric_file()
#                 total_cost = data.get("total_cost")
#                 st.write(f"Query Cost: ${cost}")
#                 st.write(f"Total Cost: ${total_cost}")

#             df = execute_sql_on_db("patient_health_data.db", sql_query)
#             st.dataframe(df)

#             if st.button("Reset"):
#                 reset_app()
#                 st.experimental_rerun()
#         except Exception as e:
#             st.error(f"An Error Occured: {e}")
import streamlit as st

st.set_page_config(
    page_title="Text-to-SQL Dashboard",
    layout="wide",
)

# -------------------------
# Load default context
# -------------------------
try:
    with open(CONTEXT_PROMPT_FILE_PATH) as f:
        default_context_prompt = f.read()
except Exception:
    default_context_prompt = ""

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.header("⚙️ Configuration")

    if "visitor_counted" not in st.session_state:
        increment_visitor_count()
        st.session_state.visitor_counted = True

    visitor_count = get_visitor_count()
    st.metric("👥 Visitor Count", visitor_count)

    use_custom_context = st.checkbox(
        "Provide custom context prompt",
        value=False,
    )

    if use_custom_context:
        context_prompt = st.text_area(
            "Context Prompt",
            height=200,
            placeholder="Enter context instructions for the LLM...",
        )
        if not context_prompt.strip():
            st.warning("Context prompt is empty.")
    else:
        context_prompt = default_context_prompt

    with st.expander("🔍 View Active Context Prompt"):
        st.write(context_prompt if context_prompt else "No context prompt set.")

# -------------------------
# Main UI
# -------------------------
st.title("🧠 Text-to-SQL Query Dashboard")
st.caption("Ask natural language questions and generate SQL queries with LLM assistance.")
st.subheader("💡 Example Questions")

example_queries = [
    "Show all patients older than 25",
    "List patients with allergies",
    "How many patients have diabetes?",
    "Get medications prescribed to patient Alice Smith",
    "Find patients with immunizations in the last year",
    "List all care plans for patients with asthma",
]

cols = st.columns(len(example_queries))

for col, query in zip(cols, example_queries):
    if col.button(query):
        st.session_state.user_prompt = query

# user_prompt = st.text_input(
#     "💬 Enter your question",
#     placeholder="e.g. Show patients with high blood pressure above 140",
# )
user_prompt = st.text_input(
    "💬 Enter your question",
    key="user_prompt",
    placeholder="e.g. Show patients with high blood pressure above 140",
)

run_query = st.button("🚀 Run Query", type="primary")

# -------------------------
# Query Execution
# -------------------------
if run_query and user_prompt.strip():

    with st.spinner("Processing your query..."):
        try:
            handler = LLMQueryHandler(
                model=GPT_MODEL,
                vector_store=VECTOR_STORE,
                embed_model=EMBED_MODEL,
                db_path=DB_PATH,
                top_k=3,
            )

            schemas = handler.get_semantic_schemas(user_prompt)
            system_prompt = sys_prompt.format(
                schemas="\n\n".join(schemas),
                context=context_prompt,
            )

            df, output = handler.process_user_query(
                schemas,
                user_prompt,
                context_prompt,
                system_prompt,
            )

            if output is None:
                st.error("❌ Failed to generate a valid SQL query.")
                st.stop()

            sql_query = output.get("SQL_QUERY")

            # Execute SQL
            df, sql_error = execute_sql_on_db("patient_health_data.db", sql_query)

            if sql_error:
                # Show detailed error in expandable box and a short warning
                st.warning("⚠️ The SQL query returned an error. Please review and try again.")
                with st.expander("View SQL Error"):
                    st.code(sql_error)
            else:
                # -------------------------
                # Tabs
                # -------------------------
                tab_results, tab_sql, tab_cost = st.tabs(
                    ["📊 Results", "🧠 Generated SQL", "💰 Cost & Metrics"]
                )

                with tab_results:
                    st.subheader("Query Results")
                    st.dataframe(df, use_container_width=True)

                with tab_sql:
                    st.subheader("Generated SQL Query")
                    st.code(sql_query, language="sql")

                with tab_cost:
                    cost = handler.calculate_query_execution_cost(
                        output.get("N_PROMPT_TOKENS", 0),
                        output.get("N_GENERATED_TOKENS", 0),
                    )
                    update_query_cost(cost)
                    data = read_metric_file()

                    col1, col2 = st.columns(2)
                    col1.metric("Query Cost ($)", f"{cost:.6f}")
                    col2.metric("Total Cost ($)", f"{data.get('total_cost', 0):.6f}")

            # -------------------------
            # Reset
            # -------------------------
            if st.button("🔄 Reset App"):
                reset_app()
                st.experimental_rerun()

        except Exception as e:
            st.error(f"⚠️ Error occurred: {e}")
