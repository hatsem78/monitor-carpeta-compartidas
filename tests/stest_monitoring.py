import os
import uuid
import tempfile
from smb.base import NotReadyError
from app.on_watch_file import OnWatchFile
from app.settings import Config, get_logger

logger = get_logger('Watcher File OnMyWatch Test')


class TestMonitoring:
    """
        Test monitoring
    """
    file_name = ''
    source = None
    destination = None

    def __init__(self, source=None, destination=None, file_name=''):

        self.source = f"/{source}/"
        self.file_name = ''
        self.destination = f"/{destination}/"

        self.file = "test.tiff"
        self.config = Config()
        self.watcher = OnWatchFile()
        self.watcher.connect_directory_monitoring()
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.basedir_files_tiff = os.path.join(basedir, "files_test/file.tiff")
        self.basedir_files_xml = os.path.join(basedir, "files_test/file.xml")

    def move_file_test(self):

        try:
            for element in range(3):
                print(element)
                uid = uuid.uuid4()
                self.file_name = f"{uid.hex}.tiff"
                file_tiff = f"/{self.source}/{self.file_name}"
                print(file_tiff)
                with open(self.basedir_files_tiff, "rb") as file:
                    self.watcher.conn.storeFile(
                        self.config.smb_watch_directory,
                        file_tiff,
                        file,
                    )

                """file_xml = f"/{self.destination}/prueba4_{uid.hex}.xml"
                print(file_xml)
                with open(self.basedir_files_tiff, "rb") as file:
                    self.watcher.conn.storeFile(
                        self.config.smb_watch_directory,
                        file_xml,
                        file,
                    )
                """
        except Exception as error:
            print(f"STORE FILE {error}")

    def move_file_test_2(self):

        try:
            for element in range(1):
                print(element)
                uid = uuid.uuid4()
                file_tiff = f"/DNI_NO_KOFAX/prueba4_{uid.hex}.tiff"
                print(file_tiff)
                with open(self.basedir_files_tiff, "rb") as file:
                    self.watcher.conn.storeFile(
                        self.config.smb_watch_directory,
                        file_tiff,
                        file,
                    )

                file_xml = f"/DNI_NO_KOFAX/prueba4_{uid.hex}.xml"
                print(file_xml)
                with open(self.basedir_files_tiff, "rb") as file:
                    self.watcher.conn.storeFile(
                        self.config.smb_watch_directory,
                        file_xml,
                        file,
                    )

        except Exception as error:
            print(f"STORE FILE {error}")

    def copy_file_samba_share(self):
        logger.info(
            f"Start file  {self.file_name} transfer: {self.file_name} "
            f" to destination {self.destination}"
        )
        contents = self.file_contents(f"{self.source}/{self.file_name}")
        if contents:
            successful_transfer = self.write_file_transfer(
                f"{self.destination}/{self.file_name}", contents
            )
            if successful_transfer:
                self.delete_remote_file()

        else:
            logger.warning(f"Filename: {self.file_name} is not read")

    def write_file_transfer(self, path, contents):
        successful_transfer = True
        try:
            with tempfile.NamedTemporaryFile() as file_obj:
                file_obj.write(contents)
                file_obj.seek(0)
                self.watcher.conn.storeFile(self.config.smb_watch_directory, path, file_obj)
            logger.info(
                f"File {self.file_name} transfer: {self.file_name} "
                f" to destination {self.destination}"
            )
        except NotReadyError as error:
            logger.warning(f"Filename: {self.file_name} is {error}")
            successful_transfer = False
        except Exception as error:
            logger.error(f"Filename: {self.file_name} read error: {error} ")
            successful_transfer = False
        return successful_transfer

    def file_contents(self, path):

        # optengo los atributos del archivo
        content = None
        try:
            attribute = self.watcher.conn.getAttributes(self.config.smb_watch_directory, path)
            logger.info(f"Attributes Filename: {attribute}")

            if attribute.file_size > 0:
                with tempfile.NamedTemporaryFile() as file_obj:
                    self.watcher.conn.retrieveFile(self.config.smb_watch_directory, path, file_obj)
                    file_obj.seek(0)
                    content = file_obj.read()
                logger.info(f"Content Filename: {attribute.filename}")
            else:
                logger.warning(f"Filename: {attribute.filename} is not size")
        except NotReadyError as error:
            logger.warning(f"Filename: {self.file_name} is {error}")
        except Exception as error:
            logger.error(f"Filename: {self.file_name} read error: {error} ")
        return content

    def delete_remote_file(self):
        try:
            self.watcher.conn.deleteFiles(
                self.config.smb_watch_directory, f"{self.source}/{self.file_name}"
            )
            logger.info(f"Delete file  {self.file_name} to source {self.source}")
        except Exception as error:
            logger.error(f"Filename: {self.file_name} read error: {error} ")


if __name__ == "__main__":
    move = TestMonitoring(source='OTROS_NO_KOFAX', destination='FilePollerTest')
    move.move_file_test()
    # move.move_file_test_2()
    move.copy_file_samba_share()
