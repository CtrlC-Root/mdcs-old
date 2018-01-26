import socket

from .generic import Node
from .http import NodeHTTPServer
from .tcp import NodeTCPServer
from .multicast import NodeMulticastServer
from .task import Task


class NodeServerConfig:
    """
    Configuration settings for a Node server.
    """

    def __init__(self, public_host, bind_host, http_port, tcp_port, mcast_port, mcast_group):
        self._public_host = public_host

        # HTTP API
        self._http_host = bind_host
        self._http_port = http_port

        # TCP API
        self._tcp_host = bind_host
        self._tcp_port = tcp_port

        # Multicast API
        self._mcast_host = bind_host
        self._mcast_port = mcast_port
        self._mcast_group = mcast_group

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
    def mcast_host(self):
        return self._mcast_host

    @property
    def mcast_port(self):
        return self._mcast_port

    @property
    def mcast_group(self):
        return self._mcast_group

    @property
    def json_dict(self):
        """
        Configuration settings in a dictionary suitable for JSON serialization.
        """

        return {
            'host': self.public_host,
            'httpPort': self.http_port,
            'tcpPort': self.tcp_port,
            'multicastPort': self.mcast_port,
            'multicastGroup': self.mcast_group}


class NodeServer:
    """
    A server that provides the APIs for interacting with a Node.
    """

    def __init__(self, config, node):
        self.config = config
        self.node = node
        self._tasks = []

        # create the HTTP server
        self._http_server = NodeHTTPServer(config, self.node)
        self.add_task(Task("HTTP API", self._http_server.run, stop=self._http_server.shutdown))

        # create the TCP server
        self._tcp_server = NodeTCPServer(config, self.node)
        self.add_task(Task("TCP API", self._tcp_server.run, stop=self._tcp_server.shutdown))

        # create the multicast server
        self._multicast_server = NodeMulticastServer(config, self.node)
        self.add_task(Task("Multicast API", self._multicast_server.run, stop=self._multicast_server.shutdown))

    @property
    def http_socket(self):
        return self._http_server.socket

    @property
    def tcp_socket(self):
        return self._tcp_server.socket

    @property
    def multicast_socket(self):
        return self._multicast_server.socket

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

        self._multicast_server.broadcast_event({"state": "STARTED"})

    def stop(self):
        """
        Stop the server.
        """

        if not self.running:
            raise RuntimeError("server is not running")

        self._multicast_server.broadcast_event({"state": "STOPPED"})
        for task in self._tasks:
            task.stop()
