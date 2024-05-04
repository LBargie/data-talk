from typing import List, Tuple
from sqlalchemy import create_engine


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
            return self.db_query_commit(
                f"CREATE TABLE llm_table AS SELECT * FROM {repr(file)}"
            )
        else:
            raise FileNotFoundError(
                "Only csv and parquet files supported at this time."
            )
