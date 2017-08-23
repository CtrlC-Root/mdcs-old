import socket

from mdcs.generic import Node
from mdcs.http import NodeHTTPServer
from mdcs.tcp import NodeTCPServer

from .task import Task


class NodeServer:
    """
    A server that provides the APIs for interacting with a Node.
    """

    def __init__(self, node, host, http_port, tcp_port):
        self.node = node
        self._tasks = []

        # update the node configuration with the server settings
        self.node.config.update({
            'httpHost': host,
            'httpPort': http_port,
            'tcpHost': host,
            'tcpPort': tcp_port
        })

        # create the HTTP server
        self._http_server = NodeHTTPServer(self.node, host, http_port)
        self.add_task(Task("HTTP API", self._http_server.run, stop=self._http_server.shutdown))

        # create the TCP server
        self._tcp_server = NodeTCPServer(self.node, host, tcp_port)
        self.add_task(Task("TCP API", self._tcp_server.run, stop=self._tcp_server.shutdown))

    @property
    def http_host(self):
        return self._http_server.host

    @property
    def http_port(self):
        return self._http_server.port

    @property
    def http_socket(self):
        return self._http_server.socket

    @property
    def tcp_host(self):
        return self._tcp_server.host

    @property
    def tcp_port(self):
        return self._tcp_server.port

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
