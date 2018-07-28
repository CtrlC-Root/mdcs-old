import sys
import time
import daemon
import signal
import logging

from .logging import LoggingConfig


class Daemon:
    """
    A daemon that runs one or more tasks in the background.
    """

    def __init__(self, logging_config=LoggingConfig(), background=False):
        self._logging_config = logging_config
        self._background = background

        self._tasks = []
        self._running = False
        self._interrupted = False
        self._logger = logging.getLogger(__name__)

    def add_task(self, task):
        """
        Add a task for the daemon to run.
        """

        self._tasks.append(task)

    def _process_signal(self, signal_number, stack_frame):
        """
        Handle a POSIX signal sent to the the daemon process.
        """

        # https://docs.python.org/3.6/library/logging.html#thread-safety
        self._interrupted = True

    def initialize_context(self):
        """
        Called just after entering the daemon context.
        """

        pass

    def finalize_context(self):
        """
        Called just before exiting the daemon context.
        """

        pass

    def run(self):
        """
        Run the daemon.
        """

        open_files = list(self._logging_config.files)
        for task in self._tasks:
            open_files.extend(task.files)

        context = daemon.DaemonContext(
            files_preserve=open_files,
            signal_map={
                signal.SIGTERM: self._process_signal,
                signal.SIGINT: self._process_signal
            })

        if not self._background:
            # run the process in the foreground
            context.detach_process = False

            # preserve standard file descriptors
            context.stdin = sys.stdin
            context.stdout = sys.stdout
            context.stderr = sys.stderr

        with context:
            # start the daemon
            self.initialize_context()
            for task in self._tasks:
                self._logger.info('starting task: %(task)s', {'task': task.name})
                task.start()

            # run until asked to stop
            while not self._interrupted:
                time.sleep(1)
                for task in self._tasks:
                    # check if the task was started but died
                    if not task.healthy:
                        self._logger.warning('detected unhealthy task: %(task)s', {'task': task.name})

                        # not sure how to fix this so just quit
                        self._interrupted = True
                        break

                    # check if the task is not running (added after we started)
                    if not task.running:
                        self._logger.info('starting task: %(task)s', {'task': task.name})
                        task.start()

            # stop the daemon
            for task in self._tasks:
                self._logger.info('stopping task: %(task)s', {'task': task.name})
                task.stop()

            self.finalize_context()
