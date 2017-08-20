import json
import socket
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

from .json import JSONEncoder
from .request import Request
from .response import Response


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
        # parse the request
        request = Request(
            url="http://{0}:{1}{2}".format(self.server.host, self.server.port, self.path),
            headers=dict(self.headers.items()),
            method=self.command)

        if 'Content-Length' in request.headers:
            data_size = int(request.headers['Content-Length'])
            request.data = self.rfile.read(data_size)

        # TODO locate the appropriate view
        # TODO run the view
        response = Response(
            headers={'Content-Type': 'application/javascript'},
            content="{'hello': 'world'}")

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
