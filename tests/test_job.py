import signal
import unittest
from datetime import timedelta
from app.job import Job, signal_handler


class TestTypeImport(unittest.TestCase):
    """
        Test TypeImport
    """

    def setUp(self):
        self.interval = 1
        self.periodic = ''
        self.execute = True
        self.job = Job(interval=timedelta(seconds=self.interval), execute=self.periodically)

    def test_run(self):
        self.job.start()
        with self.assertRaises(Exception):
            self.signal_handler()
        self.job.stop()

    def periodically(self):
        self.periodic = 'run test'
        return 1

    def periodically_error(self):
        raise TypeError('lets see if this works')

    def test_job_error(self):
        job = Job(interval=timedelta(seconds=self.interval), execute=self.periodically_error)
        job.start()
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        with self.assertRaises(Exception):
            self.periodically_error()
        job.stop()
