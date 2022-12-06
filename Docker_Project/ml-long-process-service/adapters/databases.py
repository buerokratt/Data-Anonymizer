from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from adapters import AbstractDatabase


class PostgreSQLDatabase(AbstractDatabase):
    def __init__(self, config):
        self.engine = create_engine(config.get_dst_db_connection_string(), pool_recycle=120, pool_pre_ping=True)

    def get_session(self):
        return sessionmaker(bind=self.engine)

    def read_data(self):
        raise NotImplementedError

    def write_data(self):
        raise NotImplementedError
