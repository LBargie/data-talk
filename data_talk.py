from typing import List, Tuple
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains.sql_database.query import create_sql_query_chain
from sqlalchemy import create_engine
from langchain_core.runnables import RunnableLambda
from sqlalchemy import Engine
from pydantic import BaseModel, ConfigDict
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint


class EngineModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    db_engine: Engine | None = None


class DataLoader:
    url = "duckdb:///:memory:"

    def __init__(self, **kwargs):
        self.engine = create_engine(self.url, **kwargs)
    
    def db_query_commit(self, query: str) -> None:
        with self.engine.connect() as con:
            con.exec_driver_sql(query)
            con.commit()

    def db_query(self, query: str) -> List[Tuple]:
        with self.engine.connect() as con:
            result = con.exec_driver_sql(query)
            return result.all()

    def create_table_from_file(self, file: str) -> None:
        if ".csv" in file or ".parquet" in file:
            return self.db_query_commit(f"CREATE TABLE llm_table AS SELECT * FROM {repr(file)}")
        else:
            raise FileNotFoundError("Only csv and parquet files supported at this time.")
    
        
class HuggingFaceChain:
    def __init__(self, model:str, db_engine: Engine, **kwargs):
        kwargs.setdefault("temperature", 0.1)
        self.llm = HuggingFaceEndpoint(repo_id=model, **kwargs)
        self.db_engine = EngineModel(db_engine=db_engine).db_engine

    def write_sql(self) -> str:

        self.db = SQLDatabase(engine=self.db_engine)

        return create_sql_query_chain(llm=self.llm, db=self.db)
    
    def execute_sql(self) -> str:

        return QuerySQLDataBaseTool(db=self.db)
    
    def _get_sql(self, query: str) -> str:
        "Store the generated SQL query. To be wrapped in RunnableLambda() in the SQL chain."
        
        self.get_query = query

        return query
    
    def question(self, question: str) -> str:

        chain = self.write_sql() | RunnableLambda(self._get_sql) | self.execute_sql()
        self.prompt = chain.middle[1].template

        return chain.invoke({"question": question})
