from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
import duckdb
from duckdb import DuckDBPyConnection
from langchain_core.messages import HumanMessage, SystemMessage
from dataclasses import dataclass


SYS_PROMPT = """You are a DuckDB expert. Given an input question, create a syntactically correct DuckDB SQL query to run.
"""


def create_db_from_file(filename: str) -> DuckDBPyConnection:
    db = duckdb.connect(':memory:')
    db.execute("CREATE TABLE test AS FROM read_csv($file)", {'file': filename})
    return db


@dataclass
class Context:
    conn: DuckDBPyConnection
    user_input: str


class Response(BaseModel):
    """Response when SQL could be successfully generated."""

    sql_query: str = Field(description="SQL query generated from user input")
    explanation: str = Field(
        "", description="Explanation of the SQL query, as markdown"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


structured_llm = llm.with_structured_output(Response)


@task
def table_schema(db: DuckDBPyConnection, tbl_name: str) -> str:
    """Generate schema for a table in the database."""
    result = db.execute("DESCRIBE {}".format(tbl_name))
    df = result.fetchdf()
    columns = df['column_name'].to_list()
    types = df['column_type'].to_list()
    schema = """CREATE TABLE {} (
    {})
    """.format(tbl_name, " ".join(["{} {}\n".format(col, type) for col, type in zip(columns, types)]))
    return schema


@task
def write_sql(message: str) -> Response:
    """Generate SQL query from user input."""
    return structured_llm.invoke(message)


@entrypoint()
def agent(ctx: Context) -> list:
    schema = table_schema(ctx.conn, 'test')
    sys_msg = SystemMessage(content=SYS_PROMPT + "\n" + "Use the following schema to create the query:\n" + schema.result())
    output = write_sql([sys_msg, HumanMessage(content=ctx.user_input)]).result()
    return ctx.conn.execute(output.sql_query.replace('"', "'")).fetchall()
