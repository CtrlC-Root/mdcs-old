import socket
from http.server import BaseHTTPRequestHandler, HTTPServer


class NodeHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    TODO.
    """

    def do_HEAD(self):
        """
        TODO.
        """

        # write headers
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript")
        self.end_headers()

    def do_GET(self):
        """
        TODO.
        """

        # XXX debug
        print(self.client_address)
        print(self.path)
        print(self.headers.keys())

        # write headers
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript")
        self.end_headers()

        # write response
        self.wfile.write("{'foo': 'bar'}".encode("utf-8"))


class NodeServer:
    """
    A server that provides the APIs for interacting with a Node.
    """

    def __init__(self, node, http_host, http_port):
        # store the server settings
        self.node = node

        # create the HTTP server
        self.http_server = HTTPServer((self.http_host, self.http_port), NodeHTTPRequestHandler)

    @property
    def http_host(self):
        """
        Get the host the HTTP server is bound to.
        """

        assert self.http_server.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.http_server.server_address[0]

    @property
    def http_port(self):
        """
        Get the port the HTTP server is listening on.
        """

        assert self.http_server.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.http_server.server_address[1]

    @property
    def http_socket(self):
        """
        Get the HTTP server's socket.
        """

        return self.http_server.socket

    def run(self):
        """
        Run the server.
        """

        # run the HTTP server indefinitely
        self.http_server.serve_forever()

    def stop(self):
        """
        Stop the server.
        """

        # stop the HTTP server
        self.http_server.shutdown()
