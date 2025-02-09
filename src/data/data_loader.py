from sqlalchemy import Engine


def create_table_from_file(engine: Engine, file: str) -> None:
    if ".csv" in file or ".parquet" in file:
        with engine.connect() as conn:
            conn.exec_driver_sql(
            f"CREATE TABLE llm_table AS SELECT * FROM {repr(file)}"
        )
            conn.commit()
    else:
        raise FileNotFoundError(
            "Only csv and parquet files supported at this time."
        )
