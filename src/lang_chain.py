import langchain_community.utilities.sql_database
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_core.runnables import RunnableLambda
from sqlalchemy import Engine
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from src.common import LanguageChain


class LangchainChain(LanguageChain):
    def __init__(self, model: str, db_engine: Engine, **kwargs):
        super().__init__(model, db_engine)
        kwargs.setdefault("temperature", 0.1)
        self.llm = HuggingFaceEndpoint(repo_id=self.model, **kwargs)
        self.db = langchain_community.utilities.sql_database.SQLDatabase(self.db_engine)

    def write_sql(self) -> str:
        return create_sql_query_chain(llm=self.llm, db=self.db)

    def execute_sql(self) -> str:
        return QuerySQLDataBaseTool(db=self.db)

    def get_sql(self, sql_query: str) -> str:
        "Store the generated SQL query. To be wrapped in RunnableLambda() in the SQL chain."

        self.sql_query = sql_query

        return sql_query

    def query(self, query_str: str) -> str:
        chain = self.write_sql() | RunnableLambda(self.get_sql) | self.execute_sql()
        self.prompt = chain.middle[1].template

        return chain.invoke({"question": query_str})
