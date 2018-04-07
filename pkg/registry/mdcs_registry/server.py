import socket

from .http import RegistryHTTPServer
from mdcs.task import Task


class RegistryServerConfig:
    """
    Configuration settings for a Registry server.
    """

    def __init__(self, public_host, bind_host, http_port):
        self._public_host = public_host

        # HTTP API
        self._http_host = bind_host
        self._http_port = http_port

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
    def json_dict(self):
        """
        Configuration settings in a dictionary suitable for JSON serialization.
        """

        return {'host': self.public_host, 'httpPort': self.http_port}


class RegistryServer:
    """
    A server that provides the APIs for interacting with a Registry.
    """

    def __init__(self, config, registry):
        self.config = config
        self.registry = registry
        self._tasks = []

        # create the HTTP server
        self._http_server = RegistryHTTPServer(self.config, self.registry)
        self.add_task(Task("HTTP API", self._http_server.run, stop=self._http_server.shutdown))

    @property
    def http_socket(self):
        return self._http_server.socket

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
