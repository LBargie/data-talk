from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains.sql_database.query import create_sql_query_chain
from sqlalchemy import Engine
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint


def sql_chain(model: HuggingFaceEndpoint, db: Engine):
    db = SQLDatabase(db)
    write_sql = create_sql_query_chain(llm=model, db=db) 
    execute_sql = QuerySQLDataBaseTool(db=db)
    return write_sql | execute_sql
