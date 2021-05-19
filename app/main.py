import signal
import time
from datetime import timedelta
from app.job import Job, ProgramKilled, signal_handler
from app.on_watch_file import OnWatchFile
from app.settings import get_logger

logger = get_logger('Main Watcher File')

if __name__ == "__main__":

    logger.info('Start Watcher File')
    watch = OnWatchFile()
    watch.connect_directory_monitoring()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    job = Job(interval=timedelta(seconds=watch.wait_time_seconds_job), execute=watch.periodically)
    job.start()
    while True:
        try:
            time.sleep(1)
        except ProgramKilled:
            print("Program killed: running cleanup code")
            job.stop()
            break
