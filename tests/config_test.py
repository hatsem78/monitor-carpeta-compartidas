from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.db.database_conect import Base
from app.db.models.reko_watcher import TypeImport
from app.settings import get_logger

logger = get_logger("Logger TestConfig")


class TestConfig:
    transaction = ""
    connection = ""
    engine = ""
    type_import = ""
    id_type_import = ""
    session = ""

    def setup_module(self):
        """Connection settings for database test"""
        self.engine = create_engine('sqlite:///:memory:')
        session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        self.session = session_local()
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def type_import_id(self, session, name):
        """Create type_import for instance test"""
        try:
            self.type_import = TypeImport(
                id=1,
                name=name,
            )
            session.add(self.type_import)
            self.session.flush()
            self.session.commit()

            self.id_type_import = (
                session.query(TypeImport).filter(TypeImport.name == name).first()
            )
        except SQLAlchemyError as error:
            self.session.rollback()
            logger.warning(f"Error sql database: {error.args[0]}")
        except Exception as error:
            logger.info(f"Error database table: {error}")
