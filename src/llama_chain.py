# from llama_index.core import SQLDatabase as llamadb
import llama_index.core
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.core.retrievers import NLSQLRetriever
from src.common import LanguageChain
from sqlalchemy import Engine


class LlamaChain(LanguageChain):
    def __init__(self, model: str, db_engine: Engine, **kwargs):
        super().__init__(model, db_engine)
        self.llm = HuggingFaceInferenceAPI(model_name=self.model, **kwargs)
        self.db = llama_index.core.SQLDatabase(
            self.db_engine, include_tables=["llm_table"]
        )

    def write_sql(self, query: str) -> str:
        retriever = NLSQLRetriever(
            sql_database=self.db,
            tables=["llm_table"],
            llm=self.llm,
            sql_only=True,
        )
        return retriever.retrieve(query)

    def execute_sql(self, sql_query: str) -> str:
        return self.db.run_sql(sql_query)[0]

    def get_sql(self, sql_query: str) -> str:
        return setattr(self, "sql_query", sql_query)

    def query(self, query_str: str) -> str:
        sql_query = self.write_sql(query=query_str)

        self.get_sql(sql_query[0].text)

        return self.execute_sql(self.sql_query)

