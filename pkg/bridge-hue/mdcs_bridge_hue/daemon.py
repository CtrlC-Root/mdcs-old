#!/usr/bin/env python

import socket
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from werkzeug.routing import Map, Rule


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

        # XXX
        url_parts = urllib.parse.urlparse(self.path)
        path_parts = url_parts.path.split('/')

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

        # create the URL dispatch rules
        self.url_map = Map([
            Rule('/', endpoint='status'),

            Rule('/devices', endpoint='device_list'),
            Rule('/devices/<device>', endpoint='device_detail'),
            Rule('/devices/<device>/attributes', endpoint='attribute_list'),
            Rule('/devices/<device>/attributes/<path>', endpoint='attribute_detail'),
            Rule('/devices/<device>/actions', endpoint='action_list'),
            Rule('/devices/<device>/actions/<path>', endpoint='action_detail'),

            Rule('/d', endpoint='device_list'),
            Rule('/d/<device>', endpoint='device_detail'),
            Rule('/d/<device>/at', endpoint='attribute_list'),
            Rule('/d/<device>/at/<path>', endpoint='attribute_detail'),
            Rule('/d/<device>/ac', endpoint='action_list'),
            Rule('/d/<device>/ac/<path>', endpoint='action_detail'),
        ])

        # create the HTTP server
        self.http_server = HTTPServer((http_host, http_port), NodeHTTPRequestHandler)

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

        # run the HTTP server until stopped
        self.http_server.serve_forever()

        # close the HTTP server
        self.http_server.serve_close()

    def stop(self):
        """
        Stop the server.
        """

        # stop the HTTP server in a separate thread to avoid deadlock
        # XXX: better way of doing this that avoids dangling threads?
        thread = threading.Thread(target=self.http_server.shutdown)
        thread.start()
