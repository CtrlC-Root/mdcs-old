from mdcs.http import HTTPServer
from .views import RegistryDetail, RegistryHealth, Nodes, Devices


class RegistryHTTPServer(HTTPServer):
    """
    A server that provides the HTTP API for interacting with a Registry daemon.
    """

    def __init__(self, config, registry):
        super().__init__(config.http_host, config.http_port)
        self._config = config
        self._registry = registry

        # register routes
        routes = (
            ('registry_detail', '/',       RegistryDetail),
            ('registry_health', '/health', RegistryHealth),
            ('nodes',           '/n',      Nodes),
            ('devices',         '/d',      Devices),
        )

        for name, pattern, view in routes:
            self.register_route(name, pattern, view)

    def create_context(self, request):
        return {'config': self._config, 'registry': self._registry}
