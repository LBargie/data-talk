from llama_index.core import SQLDatabase
from llama_index.core.retrievers import NLSQLRetriever


def retriever(model: str, db: SQLDatabase):
    return NLSQLRetriever(
            sql_database=db,
            tables=["llm_table"],
            llm=model,
            sql_only=True,
        )


def execute_sql(db: SQLDatabase, sql_query: str):
    return db.run_sql(sql_query)
    