from mdcs.http import HTTPServer
from .views import RegistryDetail, RegistryHealth, NodeList, DeviceList


class RegistryHTTPServer(HTTPServer):
    """
    A server that provides the HTTP API for interacting with a Registry.
    """

    def __init__(self, config, registry):
        super().__init__(config.http_host, config.http_port, {'config': config, 'registry': registry})

        # register routes
        routes = (
            ('registry_detail', '/',       RegistryDetail),
            ('registry_health', '/health', RegistryHealth),
            ('node_list',       '/n',      NodeList),
            ('device_list',     '/d',      DeviceList),
        )

        for name, pattern, view in routes:
            self.register_route(name, pattern, view)
