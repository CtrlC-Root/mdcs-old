import threading


class TaskError(RuntimeError):
    def __init__(self, task, msg):
        super().__init__("{0}: {1}".format(task.name, msg))
        self.task = task


class Task:
    """
    A named runnable task that wraps run, start, and stop functions.
    """

    def __init__(self, name, run, start=None, stop=None, files=[]):
        self._name = name
        self._run = run
        self._start = start
        self._stop = stop
        self._files = files
        self._thread = None

    @property
    def name(self):
        """
        Task name. Used to identify the background thread.
        """

        return self._name

    @property
    def files(self):
        """
        Open files that need to be preserved when daemonizing.
        """

        return self._files

    @property
    def running(self):
        return self._thread.is_alive() if self._thread else False

    def start(self):
        if self.running:
            raise TaskError(self, "task is already running")

        # signal the task to start
        if self._start is not None:
            self._start()

        # start the thread
        self._thread = threading.Thread(target=self._run, name=self.name)
        self._thread.start()

    def stop(self):
        if not self.running:
            raise TaskError(self, "task is not running")

        # signal the task to stop
        if self._stop is not None:
            self._stop()

        # stop the thread
        self._thread.join()
        self._thread = None
