from mdcs.daemon import Daemon
from mdcs.task import Task

from .http import NodeHTTPServer
from .tcp import NodeTCPServer


class NodeDaemon(Daemon):
    """
    A daemon that runs tasks necessary for a Node.
    """

    def __init__(self, config, node):
        super().__init__(background=config.background)
        self._config = config
        self._node = node

        # XXX argh
        self._node.config.update(self._config.to_json())

        # create the HTTP API server
        self._http_server = NodeHTTPServer(self._config, self._node)
        self.add_task(Task(
            "HTTP API",
            self._http_server.run,
            stop=self._http_server.shutdown,
            files=[self._http_server.socket]))

        # create the TCP API server
        self._tcp_server = NodeTCPServer(self._config, self._node)
        self.add_task(Task(
            "TCP API",
            self._tcp_server.run,
            stop=self._tcp_server.shutdown,
            files=[self._tcp_server.socket]))

        # create the discovery backend and publish task
        self._discovery_backend = self._config.discovery.create_backend()
        self.add_task(self._discovery_backend.create_publish_task())

        # publish the local node and it's devices
        registry = self._discovery_backend.publish
        registry.add_node(
            self._node.name,
            self._config.public_host,
            self._config.http_port,
            self._config.tcp_port)

        for device in self._node.devices:
            registry.add_device(device, self._node.name)
