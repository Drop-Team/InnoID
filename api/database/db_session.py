import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from api.logger import logger

Base = declarative_base()

__factory = None


def database_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("No database file specified.")

    connection_string = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    logger.info(f"Connecting to the database at {connection_string}")

    engine = sqlalchemy.create_engine(connection_string)
    __factory = orm.sessionmaker(bind=engine)

    Base.metadata.create_all(engine)


def create_session() -> orm.Session:
    global __factory
    return __factory()
