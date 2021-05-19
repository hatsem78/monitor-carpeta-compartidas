import unittest
from sqlalchemy.exc import SQLAlchemyError
from app.db.models.reko_watcher import TypeImport
from tests.config_test import TestConfig


class TestTypeImport(unittest.TestCase,  TestConfig):
    """
        Test TypeImport
    """

    def setUp(self):
        self.name = "Insert database TypeImport"
        self.setup_module()
        try:

            self.type_import = TypeImport(name=self.name, description="")
            self.session.add(self.type_import)
            self.session.flush()
        except SQLAlchemyError:
            self.session.rollback()
            raise
        finally:
            self.session.commit()

    def test_query_type_import(self):
        expected = [self.type_import]
        result = self.session.query(TypeImport).all()
        self.assertEqual(result, expected)

    def test_update_type_import(self):
        update_name = "test updates"

        try:
            self.session.query(TypeImport).filter(TypeImport.name == self.name)\
                .update(
                    {"name": update_name}
                )

            self.session.flush()
        except SQLAlchemyError:
            self.session.rollback()
            raise
        finally:
            self.session.commit()

        element = (
            self.session.query(TypeImport)
            .filter(TypeImport.name == update_name)
            .first()
        )

        self.assertEqual(update_name, element.name)

    def test_delete_type_import(self):

        delete_name = self.name

        self.session.query(TypeImport).filter(TypeImport.name == self.name).delete()
        self.session.flush()
        self.session.commit()

        element = (
            self.session.query(TypeImport)
            .filter(TypeImport.name == delete_name)
            .first()
        )
        self.assertTrue(element is None)

    def tearDown(self):
        self.session.rollback()
        self.session.close()
