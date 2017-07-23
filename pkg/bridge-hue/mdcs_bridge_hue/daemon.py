#!/usr/bin/env python

import socket
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException


class NodeHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    A handler for node HTTP API requests.
    """

    @property
    def node_server(self):
        assert hasattr(self.server, 'node_server')
        assert isinstance(self.server.node_server, NodeServer)

        return self.server.node_server

    def do_GET(self):
        """
        TODO.
        """

        # XXX
        try:
            request_url = urllib.parse.urlparse(self.path)
            endpoint, args = self.node_server.urls.match(
                path_info=request_url.path,
                method=self.command,
                query_args=request_url.query)

        except HTTPException as e:
            print(e)
            self.send_response(500)
            self.end_headers()
            return

        # write headers
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

        # write response
        self.wfile.write("endpoint: {0}\n".format(endpoint).encode("utf-8"))
        self.wfile.write("args: {0}\n".format(args).encode("utf-8"))


class NodeServer:
    """
    A server that provides the APIs for interacting with a Node.
    """

    def __init__(self, node, http_host, http_port):
        # store the server settings
        self.node = node

        # create the URL dispatch rules
        self.urls = None
        self.routes = Map([
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
        self.http_server.node_server = self

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

        try:
            # create the route adapter
            self.urls = self.routes.bind(
                server_name='{0}:{1}'.format(self.http_host, self.http_port),
                url_scheme='http')

            # run the HTTP server until stopped
            self.http_server.serve_forever()

        finally:
            # close the HTTP server
            self.http_server.server_close()

            # remove the route adapter
            self.urls = None

    def stop(self):
        """
        Stop the server.
        """

        # stop the HTTP server in a separate thread to avoid deadlock
        # XXX: better way of doing this that avoids dangling threads?
        thread = threading.Thread(target=self.http_server.shutdown)
        thread.start()
