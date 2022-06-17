import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DBLayer:

    """Слой базы данных"""

    db_config = {
        "drivername": "postgresql",
        "host": os.getenv("DB_HOST"),
        "port": 5432,
        "username": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "database": os.getenv("POSTGRES_DB"),
    }

    def __init__(self):
        self.engine = None
        self.model = declarative_base()

        self.__create_engine()

        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def __create_engine(self) -> None:
        """Создает подключение к базе данных"""
        self.engine = create_engine(URL(**DBLayer.db_config))
        self.engine.connect()


DB = DBLayer()
