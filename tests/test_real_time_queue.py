import unittest
from sqlalchemy.exc import SQLAlchemyError
from app.db.models.reko_watcher import RealTimeQueue
import datetime
from tests.config_test import TestConfig


class TestRealTimeQueuet(unittest.TestCase, TestConfig):
    """
        Test RealTimeQueuet
    """

    def setUp(self):
        self.name = "Insert database RealTimeQueue"
        self.setup_module()
        self.id_type_import = self.type_import_id(self.session, self.name)

        self.test_folder = "Test folder"
        self.test_filename = "test file name new"
        created_date = datetime.datetime.strptime(
            "2017-01-12T14:12:06.000-0500", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        try:
            self.real_time_queue = RealTimeQueue(
                type_import=self.id_type_import,
                source_folder=self.test_folder,
                filename=self.test_filename,
                created_date=created_date,
                saved_in_db_date=created_date,
                is_locked=False,
            )

            self.session.add(self.real_time_queue)
            self.session.flush()
        except SQLAlchemyError:
            self.session.rollback()
            raise
        finally:
            self.session.commit()

    def test_historic_queue_insert(self):
        test_folder = "Test folder one"
        test_filename = "test file name"

        created_date = datetime.datetime.strptime(
            "2017-01-12T14:12:06.000-0500", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        try:
            self.real_time_queue = RealTimeQueue(
                type_import=self.id_type_import,
                source_folder=test_folder,
                filename=test_filename,
                created_date=created_date,
                saved_in_db_date=created_date,
                is_locked=False,
            )

            self.session.add(self.real_time_queue)
            self.session.flush()

        except SQLAlchemyError:
            self.session.rollback()
            raise
        finally:
            self.session.commit()

        element = (
            self.session.query(RealTimeQueue)
            .filter(RealTimeQueue.source_folder == test_folder)
            .first()
        )

        self.assertEqual(test_folder, element.source_folder)

    def test_historic_queue_query(self):
        expected = [self.real_time_queue]
        result = self.session.query(RealTimeQueue).all()
        self.assertEqual(result, expected)

    def test_historic_queue_update(self):
        update_name = "New test folder"
        filename = "New test filename"
        try:
            self.session.query(RealTimeQueue).filter(
                RealTimeQueue.filename == self.test_filename
            ).update({"source_folder": update_name, 'filename': filename})

            self.session.flush()

        except SQLAlchemyError:
            self.session.rollback()
            raise
        finally:
            self.session.commit()

        element = (
            self.session.query(RealTimeQueue)
            .filter(RealTimeQueue.source_folder == update_name)
            .first()
        )

        self.assertEqual(update_name, element.source_folder)

    def test_historic_queue_delete(self):

        self.session.query(RealTimeQueue).filter(
            RealTimeQueue.source_folder == self.test_folder
        ).delete()
        self.session.flush()
        self.session.commit()

        element = (
            self.session.query(RealTimeQueue)
            .filter(RealTimeQueue.source_folder == self.test_folder)
            .first()
        )
        self.assertTrue(element is None)

    def tearDown(self):
        self.session.rollback()
        self.session.close()
