#!/usr/bin/env python

import socket
import threading

from mdcs.http import NodeHTTPServer


class NodeServer:
    """
    A server that provides the APIs for interacting with a Node.
    """

    def __init__(self, node, http_host, http_port):
        self.node = node
        self.running = False

        # create the HTTP server
        self.http_server = NodeHTTPServer(self.node, http_host, http_port)
        self.http_server_thread = threading.Thread(target=self.http_server.run)

    @property
    def http_host(self):
        """
        Get the host the HTTP server is bound to.
        """

        return self.http_server.host

    @property
    def http_port(self):
        """
        Get the port the HTTP server is listening on.
        """

        return self.http_server.port

    @property
    def http_socket(self):
        """
        Get the HTTP server's socket.
        """

        return self.http_server.socket

    def start(self):
        """
        Run the server.
        """

        if self.running:
            raise RuntimeError("server is already running")

        self.running = True

        self.http_server_thread.start()

    def stop(self):
        """
        Stop the server.
        """

        if not self.running:
            raise RuntimeError("server is not running")

        self.http_server.shutdown()
        self.http_server_thread.join()

        self.running = False
