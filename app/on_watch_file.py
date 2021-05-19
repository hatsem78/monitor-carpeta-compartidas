import socket
import copy
from datetime import datetime, timedelta
from smb.SMBConnection import SMBConnection
from smb import smb_structs
from sqlalchemy.exc import SQLAlchemyError
from app.db.database_conect import SessionLocal
from app.db.models.reko_watcher import TypeImport, RealTimeQueue
from app.settings import get_logger, Config

smb_structs.SUPPORT_SMB2 = False

logger = get_logger('Watcher File OnMyWatch')


class OnWatchFile(Config):
    """
        Class OnWatchFile monitors a certain directory with its subdirectory tree
        to identify if a new file exists
    """
    watch_directory = ''
    connected = ''
    conn = ''
    datetime_format = '%Y-%m-%d %H:%M:%S.%f'
    source_folder = ''
    file = ''
    time_diff_seconds = 0

    def __init__(self) -> None:
        super(OnWatchFile, self).__init__()
        self.session = SessionLocal()
        if self.schema != '':
            self.session.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {self.schema}")

    def connect_directory_monitoring(self):
        """shared directory monitoring connection"""

        try:
            server_ip = socket.gethostbyname(self.smb_server_name)
            self.conn = SMBConnection(
                self.smb_user_name,
                self.smb_password,
                self.smb_server_name,
                self.smb_server_name,
                '',
                use_ntlm_v2=True,
                sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,
                is_direct_tcp=True
            )
            self.connected = self.conn.connect(server_ip, 445)
            if not self.connected:
                logger.error(
                    'Authentication failed, '
                    'verify instance configuration parameters and try again.'
                )
                raise ValueError("Authentication failed")
        except Exception as error:
            logger.error(f'Can not access the system: {error}')
            raise ValueError("Can not access the system")

    def periodically(self):
        """process that runs periodically in a certain time"""
        try:
            for directory in self.smb_directory_list:  # iterate through the list of shares
                self.source_folder = directory
                list_file = self.conn.listPath(
                    self.smb_watch_directory,
                    f'/{directory}',
                    timeout=30
                )
                self.new_file_detection_monitoring(list_file)

        except Exception as error:
            logger.error(f'Periodically can not list shares: {error}')

    def new_file_detection_monitoring(self, list_file):
        """folder monitoring to detect new files."""
        try:
            for key, file in enumerate(list_file):
                self.file = copy.deepcopy(file)
                if not file.isDirectory:

                    last_write_time = self.date_format_from_times_tamp(
                        file.last_write_time
                    )

                    date_now = self.check_date_format(datetime.now())

                    # difference expressed in minutes
                    # time_diff = (date_now - last_write_time) / timedelta(
                    #    minutes=int(self.new_file_interval_time)
                    # )

                    self.time_diff_seconds = (date_now - last_write_time) / timedelta(
                        seconds=int(self.new_file_interval_time)
                    )

                    if file.file_size > 0:
                        self.insert_new_file_in_database()

        except Exception as error:
            logger.error(f'New_file_detection_monitoring can not list shares: {error}')

    def insert_new_file_in_database(self):
        """Insert new file in database"""
        try:
            id_type_import = self.session.query(TypeImport) \
                .filter(TypeImport.name == 'new_file') \
                .first()
            file_create = self.check_date_format(
                self.date_format_from_times_tamp(self.file.last_attr_change_time)
            )
            real_time_queue = RealTimeQueue(
                type_import=id_type_import.id,
                source_folder=self.source_folder,
                filename=self.file.filename,
                created_date=file_create,
                saved_in_db_date=self.check_date_format(),
                is_locked=False,
            )
            self.session.add(real_time_queue)
            self.session.flush()
            self.session.commit()
            logger.info(f'Directory: {self.source_folder}, New file :{self.file.filename},'
                        f'time:{file_create}')
        except SQLAlchemyError as error:
            self.session.rollback()
            if 'unique constraint' not in error.args[0].lower():
                logger.info(f'Error SQLAlchemyError  {error.args[0]}')
                raise ValueError('Error database')
        except Exception as error:
            logger.info(f'Error in operation: {error.args[0]}')
            raise
        finally:
            self.session.close()

    @staticmethod
    def check_date_format(date=datetime.now()):

        if date.microsecond > 0:
            result_date = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S.%f')
        else:
            result_date = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')

        return result_date

    @staticmethod
    def date_format_from_times_tamp(date=1610628721.6383548):
        result_date = datetime.fromtimestamp(date)
        return result_date
