from mdcs.task import Task
from mdcs.daemon import Daemon

from .http import RegistryHTTPServer


class RegistryDaemon(Daemon):
    """
    A server that provides the APIs for interacting with a Registry.
    """

    def __init__(self, config):
        super().__init__(logging_config=config.logging, background=config.background)
        self._config = config

        # create the discovery backend and subscribe task
        self._discovery_backend = self._config.discovery.create_backend()
        self.add_task(self._discovery_backend.create_subscribe_task())

        # create the HTTP server
        self._http_server = RegistryHTTPServer(self._config, self._discovery_backend.discovered)
        self.add_task(Task(
            "HTTP API",
            self._http_server.run,
            stop=self._http_server.shutdown,
            files=[self._http_server.socket]))
