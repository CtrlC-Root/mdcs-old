from mdcs.http import HTTPServer

from .views import NodeDetail, NodeHealth
from .views import DeviceList, DeviceDetail
from .views import AttributeDetail, AttributeValue
from .views import ActionDetail, ActionRun


class NodeHTTPServer(HTTPServer):
    """
    A server that provides the HTTP API for interacting with a Node.
    """

    def __init__(self, node):
        super().__init__(node.config.http_host, node.config.http_port)
        self._node = node

        # register routes
        routes = (
            ('node_detail',      '/',       NodeDetail),
            ('node_health',      '/health', NodeHealth),
            ('device_list',      '/d',          DeviceList),
            ('device_detail',    '/d/<device>', DeviceDetail),
            ('attribute_detail', '/d/<device>/at/<path>',   AttributeDetail),
            ('attribute_value',  '/d/<device>/at/<path>/v', AttributeValue),
            ('action_detail',    '/d/<device>/ac/<path>',   ActionDetail),
            ('action_run',       '/d/<device>/ac/<path>/r', ActionRun),
        )

        for name, pattern, view in routes:
            self.register_route(name, pattern, view)

    def create_context(self, request):
        return {'node': self._node}
