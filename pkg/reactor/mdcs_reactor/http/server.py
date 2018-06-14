from mdcs.http import HTTPServer

from .views import ReactorDetail, ReactorHealth


class ReactorHTTPServer(HTTPServer):
    """
    A server that provides the HTTP API for interacting with a Reactor daemon.
    """

    def __init__(self, config):
        super().__init__(config.http_host, config.http_port)
        self._config = config

        # register routes
        routes = (
            ('reactor_detail', '/',       ReactorDetail),
            ('reactor_health', '/health', ReactorHealth),
        )

        for name, pattern, view in routes:
            self.register_route(name, pattern, view)

    def create_context(self, request):
        return {'config': self._config}
