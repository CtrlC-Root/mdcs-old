import socket
from collections import namedtuple
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer as BaseHTTPServer

from .request import Request
from .response import Response
from .route import RoutePattern


class RouteNotFound(RuntimeError):
    pass


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """
    A handler for node HTTP API requests.
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

            # determine the appropriate route
            route, context = self.server.resolve_url(request.path)

            # update the view context with the server's view context
            context.update(self.server.view_context)

            # process the view
            view = route.view(context=context)
            response = view.handle_request(request)

            # XXX update response headers with CORS policy (defined where?)
            response.headers.update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': ','.join(view.allowed_methods),
                'Access-Control-Allow-Headers': request.headers.setdefault('Access-Control-Request-Headers', '*')
            })

        except RouteNotFound:
            response = Response(HTTPStatus.NOT_FOUND)

        except RuntimeError as e:
            response = Response(
                headers={'Content-Type': 'text/plain'},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content=str(e))

        # write the response
        self.send_response(response.status_code)
        for name, value in response.headers.items():
            self.send_header(name, value)

        self.end_headers()
        if response.content:
            self.wfile.write(response.content.encode('utf-8'))


class HTTPServer(BaseHTTPServer):
    """
    An HTTP server.
    """

    Route = namedtuple('Route', ['name', 'pattern', 'view'])

    def __init__(self, http_host, http_port, view_context={}):
        super().__init__((http_host, http_port), HTTPRequestHandler, bind_and_activate=False)
        self.allow_reuse_address = True
        self.view_context = view_context
        self.routes = {}

    @property
    def host(self):
        assert self.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.server_address[0]

    @property
    def port(self):
        assert self.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.server_address[1]

    def register_route(self, name, pattern, view):
        """
        Register a named route with a URL pattern and corresponding view.
        """

        if name in self.routes:
            raise RuntimeError("route with name {0} already registered".format(name))

        self.routes[name] = self.Route(name=name, pattern=RoutePattern(pattern), view=view)

    def resolve_url(self, path):
        """
        Determine which route corresponds to the given URL path. If a matching route is found the route antry and
        parsed variable values are returned otherwise a RouteNotFound exception is raised.
        """

        for route in self.routes.values():
            variables = route.pattern.parse(path)
            if variables is not None:
                return route, variables

        raise RouteNotFound

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
