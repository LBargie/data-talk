from pydantic_ai import Agent, RunContext
import duckdb 
from dataclasses import dataclass
from pydantic import BaseModel, Field
from duckdb import DuckDBPyConnection
import asyncio


def create_db_from_file(filename: str) -> DuckDBPyConnection:
    db = duckdb.connect(':memory:')
    db.execute("CREATE TABLE test AS FROM read_csv($file)", {'file': filename})
    return db


SYS_PROMPT = """You are a DuckDB expert. Given an input question, create a syntactically correct DuckDB SQL query to run.
Use the 'execute_sql' tool to run the query and return the results.
"""


@dataclass
class DatabaseDeps:
    tbl_name: str
    conn: DuckDBPyConnection


class Success(BaseModel):
    """Response when SQL could be successfully generated."""

    sql_query: str = Field(description="SQL query generated from user input")
    explanation: str = Field(
        "", description="Explanation of the SQL query, as markdown"
    )
    result: str = Field(description="The result of executing the SQL query in the context of the input question")


class InvalidRequest(BaseModel):
    """Response when the user input didn't include enough information to generate SQL."""

    error_message: str = Field(description="Error message explaining the issue")


Response = Success | InvalidRequest

agent: Agent[DatabaseDeps, Response] = Agent(
    'google-gla:gemini-1.5-flash',
    result_type=Response,
    deps_type=str,
    system_prompt=SYS_PROMPT,
)


@agent.system_prompt
async def system_prompt(ctx: RunContext[DatabaseDeps]) -> str:
    table = ctx.deps.tbl_name
    result = ctx.deps.conn.execute(f"DESCRIBE {table}")
    df = result.fetchdf()
    columns = df['column_name'].to_list()
    types = df['column_type'].to_list()
    schema = """CREATE TABLE {} (
    {})
    """.format(table, " ".join(["{} {}\n".format(col, type) for col, type in zip(columns, types)]))
    return f"""
Use the table information below to create the query:

{schema}
"""


@agent.tool
async def execute_sql(ctx: RunContext[DatabaseDeps], sql_query: str) -> str:
    """Excecute the SQL query.
    
    Args:
        ctx: The run context
        sql_query: The SQL query to execute
    """
    return ctx.deps.conn.execute(sql_query.replace('"', "'")).fetchall()
