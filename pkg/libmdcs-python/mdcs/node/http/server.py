from mdcs.http import HTTPServer

from .views import NodeDetail, NodeHealth
from .views import DeviceList, DeviceDetail
from .views import AttributeDetail, AttributeValue
from .views import ActionDetail, ActionRun


class NodeHTTPServer(HTTPServer):
    """
    A server that provides the HTTP API for interacting with a Node.
    """

    def __init__(self, config, node):
        super().__init__(config.http_host, config.http_port, {'config': config, 'node': node})

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
