#!/usr/bin/env python

import socket
import threading

from mdcs.http import NodeHTTPServer
from mdcs.tcp import NodeTCPServer


class NodeServer:
    """
    A server that provides the APIs for interacting with a Node.
    """

    def __init__(self, node, host, http_port, tcp_port):
        self.node = node

        # create the HTTP server
        self.http_server = NodeHTTPServer(self.node, host, http_port)
        self.http_server_thread = threading.Thread(target=self.http_server.run)

        # create the TCP server
        self.tcp_server = NodeTCPServer(self.node, host, tcp_port)
        self.tcp_server_thread = threading.Thread(target=self.tcp_server.run)

    @property
    def http_host(self):
        return self.http_server.host

    @property
    def http_port(self):
        return self.http_server.port

    @property
    def http_socket(self):
        return self.http_server.socket

    @property
    def tcp_host(self):
        return self.tcp_server.host

    @property
    def tcp_port(self):
        return self.tcp_server.port

    @property
    def tcp_socket(self):
        return self.tcp_server.socket

    @property
    def running(self):
        """
        Server is running when any thread is still alive.
        """

        return any([
            self.http_server_thread.is_alive(),
            self.tcp_server_thread.is_alive()
        ])

    @property
    def healthy(self):
        """
        Server is healthy when all the threads are alive or dead.
        """

        thread_states = set([
            self.http_server_thread.is_alive(),
            self.tcp_server_thread.is_alive()
        ])

        return len(thread_states) == 1

    def start(self):
        """
        Start the server.
        """

        if self.running:
            raise RuntimeError("server is already running")

        if not self.tcp_server_thread.is_alive():
            self.tcp_server_thread.start()

        if not self.http_server_thread.is_alive():
            self.http_server_thread.start()

    def stop(self):
        """
        Stop the server.
        """

        if not self.running:
            raise RuntimeError("server is not running")

        if self.http_server_thread.is_alive():
            self.http_server.shutdown()
            self.http_server_thread.join()

        if self.tcp_server_thread.is_alive():
            self.tcp_server.shutdown()
            self.tcp_server_thread.join()
