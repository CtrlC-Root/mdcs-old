import socket

from mdcs.generic import Node
from mdcs.task import Task

from .http import NodeHTTPServer
from .tcp import NodeTCPServer


class NodeServerConfig:
    """
    Configuration settings for a Node server.
    """

    def __init__(self, public_host, bind_host, http_port, tcp_port):
        self._public_host = public_host

        # HTTP API
        self._http_host = bind_host
        self._http_port = http_port

        # TCP API
        self._tcp_host = bind_host
        self._tcp_port = tcp_port

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
    def tcp_host(self):
        return self._tcp_host

    @property
    def tcp_port(self):
        return self._tcp_port

    @property
    def json_dict(self):
        """
        Configuration settings in a dictionary suitable for JSON serialization.
        """

        return {'host': self.public_host, 'httpPort': self.http_port, 'tcpPort': self.tcp_port}


class NodeServer:
    """
    A server that provides the APIs for interacting with a Node.
    """

    def __init__(self, config, node):
        self.config = config
        self.node = node
        self._tasks = []

        # create the HTTP server
        self._http_server = NodeHTTPServer(self.config, self.node)
        self.add_task(Task("HTTP API", self._http_server.run, stop=self._http_server.shutdown))

        # create the TCP server
        self._tcp_server = NodeTCPServer(self.config, self.node)
        self.add_task(Task("TCP API", self._tcp_server.run, stop=self._tcp_server.shutdown))

    @property
    def http_socket(self):
        return self._http_server.socket

    @property
    def tcp_socket(self):
        return self._tcp_server.socket

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
