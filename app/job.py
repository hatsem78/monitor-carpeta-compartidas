import threading


class ProgramKilled(Exception):
    pass


def signal_handler(signum, frame):
    raise ProgramKilled


class Job(threading.Thread):
    """
          Class Job that launches monitoring with an estimated time
          ...
          Attributes
          ----------
          interval : int: required
            interval represents the time interval to launch each process
          execute: obj: required
            execute represents the function to be executed in each process
      """
    def __init__(self, interval, execute, *args, **kwargs) -> None:
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        """stop cancels the processes and waits for all to finish"""
        self.stopped.set()
        self.join()

    def run(self):
        """wait to execute again that all processes have been terminated in case of any error"""
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)
