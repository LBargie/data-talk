from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine


class EngineModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    db_engine: Engine


class LanguageChain(ABC):
    def __init__(self, model: str, db_engine: Engine):
        self.model = model
        self.db_engine = EngineModel(db_engine=db_engine).db_engine

    @abstractmethod
    def query(self) -> str:
        pass

    @abstractmethod
    def write_sql(self) -> str:
        pass

    @abstractmethod
    def execute_sql(self) -> str:
        pass

    @abstractmethod
    def get_sql(self) -> None:
        pass
