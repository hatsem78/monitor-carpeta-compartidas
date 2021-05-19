import cx_Oracle
import os
import pathlib
import time
from dotenv import load_dotenv
from logging import Formatter, Logger, StreamHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))
# Extensions formats for Tesseract
allowed_ext = {'png', 'pdf', 'jpeg', 'jpg'}
# Extensions formats for Barcodes
allowed_ext_barcode_qr = {'tiff', 'tif'}
allowed_ext_barcode_pdf417 = {'png', 'jpeg', 'jpg'}

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    __dialect = ''
    __username = ''
    __password = ''
    __schema = ''
    __host = ''
    __port = ''
    __service_name = ''
    __system = ''
    __smb_watch_directory = ''
    __smb_server_name = ''
    __smb_user_name = ''
    __smb_password = ''
    __smb_directory_list = ''
    __creation_file_time_difference = ''
    __new_file_interval_time = 2
    __wait_time_seconds_job = 1
    __logging_level = False
    __url_engine = ''

    def __init__(self):
        """
            Environment Variable system
        """
        self.host = os.getenv('ORACLE_HOST', '')
        self.dialect = os.getenv('SQL_DIALECT', '')
        self.sql_driver = os.getenv('SQL_DRIVER', '')
        self.username = os.getenv('ORACLE_USER_NAME', '')
        self.service_name = os.getenv('ORACLE_SERVICE_NAME', '')
        self.port = os.getenv('ORACLE_PORT', '')
        self.password = os.getenv('PASSWORD_ORACLE', '')
        self.schema = os.getenv('ORACLE_SCHEMA', '')

        self.smb_server_name = os.getenv('SMB_SERVER_NAME', '')
        self.smb_user_name = os.getenv('SMB_USER_NAME', '')
        self.smb_password = os.getenv('SMB_PASSWORD', '')
        self.smb_watch_directory = os.getenv("SMB_WATCH_DIRECTORY", '')
        self.smb_directory_list = os.getenv("DIRECTORY_LIST", 'ALL')
        self.system = os.getenv("SYSTEM", "linux")
        self.wait_time_seconds_job = os.getenv("WAIT_TIME_SECONDS_JOB", '1')
        self.new_file_interval_time = os.getenv("NEW_FILE_INTERVAL_TIME", '2')
        self.testing = os.getenv("NOT_TESTING", 'False')
        if self.system == "windows":
            self.lib_dir = f"{pathlib.Path(__file__).parent.parent.absolute()}" \
                           f"\\db\\instantclient_oracle_windows"

    @property
    def testing(self):
        return self.__testing

    @testing.setter
    def testing(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("testing must be str")
        self.__testing = True if value == 'True' else False

    @property
    def smb_password(self):
        return self.__smb_password

    @smb_password.setter
    def smb_password(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("smb_password must be str")
        self.__smb_password = value

    @property
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("schema must be str")
        self.__schema = value

    @property
    def smb_user_name(self):
        return self.__smb_user_name

    @smb_user_name.setter
    def smb_user_name(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("smb_server_name must be str")
        self.__smb_user_name = value

    @property
    def smb_server_name(self):
        return self.__smb_server_name

    @smb_server_name.setter
    def smb_server_name(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("smb_server_name must be str")
        self.__smb_server_name = value

    @property
    def dialect(self):
        return self.__dialect

    @dialect.setter
    def dialect(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("dialect must be str")
        self.__dialect = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("username must be str")
        self.__username = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("password must be str")
        self.__password = value

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("host must be str")
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("port must be str")
        self.__port = value

    @property
    def service_name(self):
        return self.__service_name

    @service_name.setter
    def service_name(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("service_name must be str")
        self.__service_name = value

    @property
    def system(self):
        return self.__system

    @system.setter
    def system(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("service_name must be str")
        self.__system = value

    @property
    def smb_watch_directory(self):
        return self.__smb_watch_directory

    @smb_watch_directory.setter
    def smb_watch_directory(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("smb_watch_directory must be str")
        self.__smb_watch_directory = value

    @property
    def smb_directory_list(self):
        return self.__smb_directory_list

    @smb_directory_list.setter
    def smb_directory_list(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("smb_directory_list must be list")
        self.__smb_directory_list = value.replace(" ", "").split(',') \
            if type(value) == str else [value]

    @property
    def new_file_interval_time(self):
        return self.__new_file_interval_time

    @new_file_interval_time.setter
    def new_file_interval_time(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("smb_watch_directory must be str")
        self.__new_file_interval_time = value

    @property
    def wait_time_seconds_job(self):
        return self.__wait_time_seconds_job

    @wait_time_seconds_job.setter
    def wait_time_seconds_job(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("wait_time_seconds_job must be str")
        self.__wait_time_seconds_job = int(value)

    @property
    def url_engine(self):
        if self.testing:
            dsn = cx_Oracle.makedsn(
                self.host,
                str(self.port),
                service_name=self.service_name
            )

            self.__url_engine = f'{self.dialect}+{self.sql_driver}:' \
                                f'//{self.username}:{self.password}@{dsn}'
        else:
            self.__url_engine = 'sqlite:///:memory:'
        return self.__url_engine

    @url_engine.setter
    def url_engine(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("url_engine must be str")
        self.__url_engine = value


def get_logger(name):
    """
        Configuration logger for sonar
    """
    level = os.getenv("LOGGING_LEVEL", "DEBUG")

    message_format = "[%(asctime)s] [%(levelname)s] %(message)s"
    timestamp_format = "%Y-%m-%dT%H:%M:%SZ"

    formatter = Formatter(fmt=message_format, datefmt=timestamp_format)
    formatter.converter = time.gmtime

    handler = StreamHandler()
    handler.setFormatter(formatter)

    logger = Logger(name, level=level)
    logger.addHandler(handler)

    return logger


def logger_call_message(logger=None, type_logger='info', message='', additional=''):
    message = f'{message.upper()}{additional}'
    if type_logger == 'info':
        logger.info(message)
    elif type_logger == 'error':
        logger.error(message)
    elif type_logger == 'warning':
        logger.warning(message)

    return True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext


def allowed_file_barqr(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext_barcode_qr


def allowed_file_bar417(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext_barcode_pdf417
