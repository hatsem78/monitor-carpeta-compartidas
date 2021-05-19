import unittest
from app.db.models.reko_watcher import HistoricQueue
import datetime
from tests.config_test import TestConfig


class TestHistoricQueue(unittest.TestCase, TestConfig):

    def setUp(self):
        self.name = 'Insert database'
        self.setup_module()

        self.id_type_import = self.type_import_id(self.session, self.name)

        self.test_folder = "Test folder"

        created_date = datetime.datetime.strptime(
            '2017-01-12T14:12:06.000-0500',
            '%Y-%m-%dT%H:%M:%S.%f%z'
        )

        self.real_time_queue = HistoricQueue(
            type_import=self.id_type_import,
            source_folder=self.test_folder,
            filename="test file name",
            created_date=created_date,
            saved_in_db_date=created_date,
            locked_date=created_date,
        )

        self.session.add(self.real_time_queue)
        self.session.flush()
        self.session.commit()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_historic_queue_insert(self):
        test_folder = "Test folder one"

        created_date = datetime.datetime.strptime(
            '2017-01-12T14:12:06.000-0500',
            '%Y-%m-%dT%H:%M:%S.%f%z'
        )

        real_time_queue = HistoricQueue(
            type_import=self.id_type_import,
            source_folder=test_folder,
            filename="test file name new",
            created_date=created_date,
            saved_in_db_date=created_date,
            locked_date=created_date,
            finish_transfer_date=created_date
        )

        self.session.add(real_time_queue)
        self.session.flush()
        self.session.commit()

        element = self.session.query(HistoricQueue) \
            .filter(HistoricQueue.source_folder == test_folder) \
            .first()

        self.assertEqual(test_folder, element.source_folder)

    def test_est_historic_queue_query(self):
        expected = [self.real_time_queue]
        result = self.session.query(HistoricQueue).all()
        self.assertEqual(result, expected)

    def test_est_historic_queue_update(self):
        update_name = 'New test folder '

        self.session.query(HistoricQueue).filter(
            HistoricQueue.source_folder == self.test_folder
        ).update(
            {"source_folder": update_name}
        )

        self.session.flush()
        self.session.commit()

        element = self.session.query(HistoricQueue) \
            .filter(HistoricQueue.source_folder == update_name) \
            .first()

        self.assertEqual(update_name, element.source_folder)

    def test_est_historic_queue_delete(self):

        self.session.query(HistoricQueue).filter(
            HistoricQueue.source_folder == self.test_folder
        ).delete()
        self.session.flush()
        self.session.commit()

        element = self.session.query(HistoricQueue) \
            .filter(HistoricQueue.source_folder == self.test_folder) \
            .first()
        self.assertTrue(element is None)
