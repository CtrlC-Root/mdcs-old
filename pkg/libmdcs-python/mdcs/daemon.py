import sys
import time
import daemon
import signal


class TaskDaemon:
    """
    A daemon that runs one or more tasks in the background.
    """

    def __init__(self, background=False):
        self._background = background

        self._tasks = []
        self._running = False
        self._interrupted = False

    def add_task(self, task):
        """
        Add a task for the daemon to run.
        """

        self._tasks.append(task)

    def _process_signal(self, signal_number, stack_frame):
        """
        Handle a POSIX signal sent to the the daemon process.
        """

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

        context = daemon.DaemonContext(
            files_preserve=sum(map(lambda t: t.files, self._tasks), []),
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
                task.start()

            # run until asked to stop
            while not self._interrupted:
                time.sleep(1)
                for task in self._tasks:
                    # check if the task was started but died
                    if not task.healthy:
                        # XXX something is broken, let's shut down
                        self._interrupted = True
                        break

                    # check if the task is not running (added after we started)
                    if not task.running:
                        task.start()

            # stop the daemon
            for task in self._tasks:
                task.stop()

            self.finalize_context()
