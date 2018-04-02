import socket
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

from mdcs.http.request import Request
from mdcs.http.response import Response
from mdcs.http.route import Route, RouteMap, RouteNotFound
from .views import RegistryDetail, RegistryHealth, NodeList, DeviceList


class RegistryHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    A handler for registry HTTP API requests.
    """

    def do_OPTIONS(self):
        self.do_GENERIC()

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

            # determine the appropriate view
            route_name, route_variables = self.server.route_map.parse(request.path)
            view_class = self.server.view_map[route_name]

            # run the view
            route_variables['config'] = self.server.config
            route_variables['registry'] = self.server.registry

            view = view_class(context=route_variables)
            response = view.handle_request(request)

        except RouteNotFound:
            response = Response(HTTPStatus.NOT_FOUND)

        except RuntimeError as e:
            response = Response(
                headers={'Content-Type': 'text/plain'},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content=str(e))

        # XXX update response headers with CORS policy
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': ','.join(view.allowed_methods),
            'Access-Control-Allow-Headers': request.headers.setdefault('Access-Control-Request-Headers', '*')
        })

        # write the response
        self.send_response(response.status_code)
        for name, value in response.headers.items():
            self.send_header(name, value)

        self.end_headers()
        if response.content:
            self.wfile.write(response.content.encode('utf-8'))


class RegistryHTTPServer(HTTPServer):
    """
    A server that provides the HTTP API for interacting with a Registry.
    """

    def __init__(self, config, registry):
        super().__init__((config.http_host, config.http_port), RegistryHTTPRequestHandler, bind_and_activate=False)
        self.allow_reuse_address = True

        # store the server settings
        self.config = config
        self.registry = registry

        # create the view map
        self.view_map = {
            'registry_detail': RegistryDetail,
            'registry_health': RegistryHealth,

            'node_list': NodeList,
            'device_list': DeviceList,
        }

        # create the route map
        self.route_map = RouteMap(routes={
            'registry_detail': '/',
            'registry_health': '/health',

            'node_list':   '/n',
            'device_list': '/d',
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
