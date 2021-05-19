import os
import time
from logging.config import dictConfig

from dotenv import load_dotenv
from logging import Formatter, Logger, StreamHandler

# Extensions formats for Tesseract
allowed_ext = {'png', 'pdf', 'jpeg', 'jpg'}
# Extensions formats for Barcodes
allowed_ext_barcode_qr = {'tiff', 'tif'}
allowed_ext_barcode_pdf417 = {'png', 'jpeg', 'jpg'}

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext


def allowed_file_barqr(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext_barcode_qr


def allowed_file_bar417(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext_barcode_pdf417


class Config(object):
    __pytesseract_linux = ''
    __tesseract_cmd = ''
    __disable_3rd_party_logs = 'TRUE'

    def __init__(self):
        """
            Environment Variable system
        """
        self.pytesseract_linux = os.getenv('PYTESSERACT', 'False')
        self.tesseract_cmd = os.getenv('PYTESSERACT_CMD', 'tesseract')
        self.disable_3rd_party_logs = os.getenv('DISABLE_3RD_PARTY_LOGS', 'true')

    @property
    def pytesseract_linux(self):
        return self.__pytesseract_linux

    @pytesseract_linux.setter
    def pytesseract_linux(self, value):
        if value is None:
            raise TypeError("pytesseract_linux is not None")
        elif not isinstance(value, (str,)):
            raise TypeError("pytesseract_linux must be str")
        self.__pytesseract_linux = True if value == 'True' else False

    @property
    def tesseract_cmd(self):
        return self.__tesseract_cmd

    @tesseract_cmd.setter
    def tesseract_cmd(self, value):
        if value is None:
            raise TypeError("tesseract_cmd is not None")
        elif not isinstance(value, (str,)):
            raise TypeError("tesseract_cmd must be str")
        self.__tesseract_cmd = value

    @property
    def disable_3rd_party_logs(self):
        return self.__disable_3rd_party_logs

    @disable_3rd_party_logs.setter
    def disable_3rd_party_logs(self, value):
        if value is None:
            raise ValueError("disable_3rd_party_logs not must be str")
        elif not isinstance(value, (str,)):
            raise ValueError("disable_3rd_party_logs must be str")
        self.__disable_3rd_party_logs = True if value.lower() == 'true' else False


def get_logger(name):
    config = Config()

    if config.disable_3rd_party_logs:

        dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
        })

    level = os.getenv("LOGGING_LEVEL", "DEBUG")

    message_format = "[%(asctime)s] [%(levelname)s] %(message)s"
    timestamp_format = "%Y-%m-%dT%H:%M:%S"

    formatter = Formatter(fmt=message_format, datefmt=timestamp_format)
    formatter.converter = time.gmtime

    handler = StreamHandler()
    handler.setFormatter(formatter)

    logger = Logger(name, level=level)
    logger.addHandler(handler)

    return logger
