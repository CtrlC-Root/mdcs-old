import socket

from .http import RegistryHTTPServer
from mdcs.task import Task


class RegistryServerConfig:
    """
    Configuration settings for a Registry server.
    """

    def __init__(self, public_host, bind_host, http_port, discovery):
        self._public_host = public_host

        # HTTP API
        self._http_host = bind_host
        self._http_port = http_port

        # Discovery
        self._discovery = discovery

    @property
    def public_host(self):
        return self._public_host

    @property
    def http_host(self):
        return self._http_host

    @property
    def http_port(self):
        return self._http_port

    @property
    def discovery(self):
        return self._discovery

    def to_json(self):
        """
        Configuration settings in a dictionary suitable for JSON serialization.
        """

        return {
            'host': self.public_host,
            'httpPort': self.http_port,
            'discovery': self.discovery.to_json()}


class RegistryServer:
    """
    A server that provides the APIs for interacting with a Registry.
    """

    def __init__(self, config):
        self.config = config
        self._tasks = []

        # create the discovery backend and subscribe task
        self._discovery_backend = self.config.discovery.create_backend()
        self.add_task(self._discovery_backend.create_subscribe_task())

        # create the HTTP server
        self._http_server = RegistryHTTPServer(self.config, self._discovery_backend.discovered)
        self.add_task(Task(
            "HTTP API",
            self._http_server.run,
            stop=self._http_server.shutdown,
            files=[self._http_server.socket]))

    @property
    def files(self):
        """
        Open files that need to be preserved when daemonizing.
        """

        return [file for task_files in map(lambda t: t.files, self._tasks) for file in task_files]

    def add_task(self, task):
        """
        Add a task to the server and start or stop it as necessary to match the server state.
        """

        start_task = self.running and (not task.running)
        stop_task = (not self.running) and task.running

        self._tasks.append(task)
        if start_task:
            task.start()

        elif stop_task:
            task.stop()

    @property
    def running(self):
        """
        Server is running when any task is still running.
        """

        return any(map(lambda t: t.running, self._tasks))

    @property
    def healthy(self):
        """
        Server is healthy when all the tasks are running or stopped.
        """

        thread_states = set(map(lambda t: t.running, self._tasks))
        return len(thread_states) == 1

    def start(self):
        """
        Start the server.
        """

        if self.running:
            raise RuntimeError("server is already running")

        for task in self._tasks:
            task.start()

    def stop(self):
        """
        Stop the server.
        """

        if not self.running:
            raise RuntimeError("server is not running")

        for task in self._tasks:
            task.stop()
