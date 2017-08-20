import socket
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

from .json import JSONEncoder
from .request import Request
from .response import Response
from .route import Route, RouteMap, RouteNotFound
from .views import NodeDetail, NodeHealth


class NodeHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    A handler for node HTTP API requests.
    """

    def do_HEAD(self):
        self.do_GENERIC()

    def do_GET(self):
        self.do_GENERIC()

    def do_POST(self):
        self.do_GENERIC()

    def do_PUT(self):
        self.do_GENERIC()

    def do_DELETE(self):
        self.do_GENERIC()

    def do_GENERIC(self):
        try:
            # parse the request
            request = Request(
                url="http://{0}:{1}{2}".format(self.server.host, self.server.port, self.path),
                headers=dict(self.headers.items()),
                method=self.command)

            if 'Content-Length' in request.headers:
                data_size = int(request.headers['Content-Length'])
                request.data = self.rfile.read(data_size)

            # TODO determine the appropriate view
            route_name, route_variables = self.server.route_map.parse(request.path)
            view_class = self.server.view_map[route_name]

            # TODO run the view
            view = view_class()
            response = view.handle_request(request)

        except RouteNotFound:
            response = Response(HTTPStatus.NOT_FOUND)

        except RuntimeError as e:
            response = Response(
                headers={'Content-Type': 'text/plain'},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content=str(e))

        # XXX update response with CORS policy
        response.headers['Access-Control-Allow-Origin'] = '*'

        # write the response
        self.send_response(response.status_code)
        for name, value in response.headers.items():
            self.send_header(name, value)

        self.end_headers()
        if response.content:
            self.wfile.write(response.content.encode('utf-8'))


class NodeHTTPServer(HTTPServer):
    """
    A server that provides the HTTP API for interacting with a Node.
    """

    def __init__(self, node, host, port):
        super().__init__((host, port), NodeHTTPRequestHandler, bind_and_activate=False)

        # store the server settings
        self.node = node

        # create the view map
        self.view_map = {
            'node_detail': NodeDetail,
            'node_health': NodeHealth,

            # 'device_list': DeviceList,
            # 'device_detail': DeviceDetail,
            # 'attribute_detail': AttributeDetail,
            # 'attribute_value': AttributeValue,
            # 'action_detail': ActionDetail,
            # 'action_run': ActionRun
        }

        # create the route map
        self.route_map = RouteMap(routes={
            'node_detail': '/',
            'node_health': '/health',

            'device_list':      '/d',
            'device_detail':    '/d/<device>',
            'attribute_detail': '/d/<device>/at/<path>',
            'attribute_value':  '/d/<device>/at/<path>/v',
            'action_detail':    '/d/<device>/ac/<path>',
            'action_run':       '/d/<device>/ac/<path>/r',
        })

    @property
    def host(self):
        assert self.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.server_address[0]

    @property
    def port(self):
        assert self.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.server_address[1]

    def run(self):
        try:
            # bind and activate the HTTP server
            self.server_bind()
            self.server_activate()

            # process HTTP requests until stopped
            self.serve_forever()

        finally:
            # close the HTTP server
            self.server_close()

            # remove the route adapter
            self.urls = None
