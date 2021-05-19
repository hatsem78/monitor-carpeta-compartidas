from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import get_logger, Config

logger = get_logger('Connection database')
config = Config()

"""
    Database connection that is then used throughout the project
"""

try:
    engine = create_engine(
        config.url_engine,
        echo=False,
        max_identifier_length=30,
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

except Exception as err:
    logger.error(f"Error connecting: cx_Oracle.init_oracle_client() {err}")
