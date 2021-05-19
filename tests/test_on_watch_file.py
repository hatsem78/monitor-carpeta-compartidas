import os
import time
import unittest
from collections import namedtuple
import mock
from datetime import datetime
from testfixtures import should_raise
from app.on_watch_file import OnWatchFile
from app.settings import Config
from tests.config_test import TestConfig


class TesOnWatchFile(unittest.TestCase, TestConfig):
    """
        Test OnWatchFile
    """

    def setUp(self):
        self.file = "test.tiff"
        self.setup_module()
        self.config = Config()
        self.config.schema = ''
        self.on_watch_file = OnWatchFile()
        self.on_watch_file.session = self.session

        basedir = os.path.abspath(os.path.dirname(__file__))
        self.basedir_monitoring = os.path.join(basedir, "monitoring")
        self.basedir_files_tiff = os.path.join(basedir, "files_test/file.tiff")
        self.basedir_files_xml = os.path.join(basedir, "files_test/file.xml")
        list_file = [
            {
                "alloc_size": 0,
                "create_time": 1606743144.2058148,
                "file_attributes": 16,
                "file_id": None,
                "file_size": 0,
                "filename": ".",
                "isDirectory": True,
                "isNormal": False,
                "isReadOnly": False,
                "last_access_time": 1608919592.1831565,
                "last_attr_change_time": 1608919592.1831565,
                "last_write_time": 1608919592.1831565,
                "short_name": "",
            },
            {
                "alloc_size": 0,
                "create_time": 1606743144.2058148,
                "file_attributes": 16,
                "file_id": None,
                "file_size": 0,
                "filename": "",
                "isDirectory": True,
                "isNormal": False,
                "isReadOnly": False,
                "last_access_time": 1608919592.1831565,
                "last_attr_change_time": 1608919592.1831565,
                "last_write_time": 1608919592.1831565,
                "short_name": "",
            },
            {
                "alloc_size": 1798144,
                "create_time": float(time.time()),
                "file_attributes": 32,
                "file_id": None,
                "file_size": 1797347,
                "filename": "file.tiff",
                "isDirectory": False,
                "isNormal": False,
                "isReadOnly": False,
                "last_access_time": float(time.time()),
                "last_attr_change_time": float(time.time()),
                "last_write_time": float(time.time()),
                "short_name": "",
            },
        ]
        self.list_file = []
        for key, element in enumerate(list_file):
            self.list_file.append(
                namedtuple("SharedFile", element.keys())(*element.values())
            )

        self.id_type_import = self.type_import_id(self.session, "new_file")

    def test_new_file_detection_monitoring(self):
        """Test new file detection monitoring"""
        self.on_watch_file.source_folder = "TestDirectory"
        self.on_watch_file.new_file_detection_monitoring(self.list_file)
        self.assertTrue(self.on_watch_file.file in self.list_file)

    def test_new_file_detection_monitoring_exception(self):
        """Test new file detection monitoring exception"""
        self.on_watch_file.source_folder = []

        with self.assertRaises(Exception) as context:
            self.on_watch_file.new_file_detection_monitoring([1, 2])
            self.assertTrue(Exception in context.expected)

    def test_insert_new_file_in_database(self):
        """Test new file detection monitoring"""
        self.on_watch_file.source_folder = "TestDirectory"
        self.on_watch_file.file = self.list_file[2]
        self.on_watch_file.insert_new_file_in_database()
        self.assertTrue(self.on_watch_file.file in self.list_file)

    def test_insert_new_file_in_database_exception(self):
        """Test insert new file in database Exception"""
        self.on_watch_file.source_folder = "TestDirectory"
        self.on_watch_file.file = []

        setattr(self.on_watch_file, "file.create_time", '')

        with self.assertRaises(Exception) as context:
            self.on_watch_file.insert_new_file_in_database()
            self.assertTrue(Exception in context.expected)

    @should_raise(ValueError('Error database'))
    def test_insert_new_file_in_database_exception_error_database(self):
        """Test insert new file in database SQLAlchemyError """
        self.on_watch_file.source_folder = "TestDirectory"
        files = [
            {
                "alloc_size": 1798144,
                "create_time": float(time.time()),
                "file_attributes": 32,
                "file_id": None,
                "file_size": 1797347,
                "filename": None,
                "isDirectory": False,
                "isNormal": False,
                "isReadOnly": False,
                "last_access_time": float(time.time()),
                "last_attr_change_time": float(time.time()),
                "last_write_time": float(time.time()),
                "short_name": "",
            },
        ]
        list_file = []
        for key, element in enumerate(files):
            list_file.append(
                namedtuple("SharedFile", element.keys())(*element.values())
            )

        self.on_watch_file.file = list_file[0]
        self.on_watch_file.insert_new_file_in_database()
        self.on_watch_file.insert_new_file_in_database()

    def test_connect_directory_monitoring_exception(self):
        """Test connect directory monitoring Exception """
        watcher = OnWatchFile()
        watcher.smb_server_name = 'localhost'
        watcher.password = ''
        watcher.connected = False
        with self.assertRaises(Exception) as context:
            watcher.connect_directory_monitoring()
            self.assertTrue(Exception in context.expected)

    @should_raise(ValueError("Can not access the system"))
    def test_connect_directory_monitoring_not_access(self):
        """Test connect directory monitoring Exception """
        watcher = OnWatchFile()
        watcher.smb_server_name = 'localhost'
        watcher.connect_directory_monitoring()

    @mock.patch('app.on_watch_file.OnWatchFile.connect_directory_monitoring')
    @mock.patch('socket.gethostbyname')
    def test_connect_directory_monitoring(self, mocked_get, mock_conn):
        mock_conn.return_value = True
        mocked_get.return_value = '127.0.0.1'
        watcher = OnWatchFile()
        watcher.smb_server_name = '127.0.0.1'
        watcher.smb_user_name = 'tests_user'
        watcher.smb_server_name = 'gdafsrvdesa01.ar.bsch'
        smb = watcher.connect_directory_monitoring()

        self.assertTrue(smb)

    @should_raise(ValueError("Can not access the system"))
    def test_connect_directory_monitoring_value_error(self):
        """Test connect directory monitoring ValueError"""
        watcher = OnWatchFile()
        watcher.smb_user_name = 'tests_user'
        watcher.smb_server_name = 'gdafsrvdesa01.ar.bsch'

        watcher.connect_directory_monitoring()

    def test_periodically(self):
        """Test Periodically"""
        self.on_watch_file.smb_directory_list = 'OTROS_NO_KOFAX, DNI_NO_KOFAX'

        watcher = self.on_watch_file.periodically()
        self.assertFalse(watcher)

    def test_periodically_exception(self):
        """Test Periodically Exception"""
        self.on_watch_file.smb_directory_list = ''

        with self.assertRaises(Exception) as context:
            self.on_watch_file.periodically()
            self.assertTrue(Exception in context.expected)

    def test_check_date_format_return_now(self):
        result_date = self.on_watch_file.check_date_format()
        self.assertTrue(datetime.now(), result_date)

    def test_check_date_format_return_microsecond(self):
        result_date = self.on_watch_file.check_date_format(datetime.now())
        self.assertTrue(datetime.now(), result_date)

    def test_check_date_format_return_not_microsecond(self):
        date = datetime.strptime('2021-01-14 09:44:42', '%Y-%m-%d %H:%M:%S')
        result_date = self.on_watch_file.check_date_format(date)
        self.assertTrue(result_date, date)

    def test_date_format_from_times_tamp(self):
        date = 1610628721.6383548
        result_date = self.on_watch_file.date_format_from_times_tamp(date)
        self.assertTrue(result_date, date)

    def tearDown(self):
        self.session.rollback()
        self.session.close()
