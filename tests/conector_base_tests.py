import unittest
from sqlalchemy.exc import SQLAlchemyError
from app.db.database_conect import SessionLocal
from app.db.models.reko_watcher import TypeImport


class TestHistoricQueue(unittest.TestCase):
    def setUp(self):
        self.session = SessionLocal()

    def tearDown(self):
        self.session.close()

    def test_historic_queue_insert(self):
        try:
            self.session.execute("ALTER SESSION SET CURRENT_SCHEMA = REKO")
            """
            self.session.execute(f"ALTER SESSION SET CURRENT_SCHEMA = REKO")
            self.session.query(TypeImport).filter(
                TypeImport.name == 'email'
            ).update({"name": 'new_file', "description": 'Identification of a new file'})
            self.session.flush()
            self.session.commit()
            """
            type_import = TypeImport(
                name="new_file", description="Identification of a new file"
            )

            self.session.add(type_import)
            self.session.flush()
            self.session.commit()

            self.id_type_import = self.session.query(TypeImport).first()
            print(self.id_type_import)

        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            print(error)
