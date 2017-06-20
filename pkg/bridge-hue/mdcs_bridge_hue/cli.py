#!/usr/bin/env python

import sys
import daemon
import signal
import lockfile
import argparse

from http.server import BaseHTTPRequestHandler, HTTPServer


class BridgeAPIHandler(BaseHTTPRequestHandler):
    """
    TODO.
    """

    pass


class BridgeNode:
    """
    A bridge node daemon.
    """

    def __init__(self, host, port):
        # HTTP settings
        self.host = host
        self.port = port

        # HTTP server
        self.http_server = HTTPServer((self.host, self.port), BridgeAPIHandler)

    @property
    def http_socket(self):
        """
        XXX.
        """

        return self.http_server.socket

    def run(self):
        """
        Run the node.
        """

        # run the HTTP server indefinitely
        self.http_server.serve_forever()

    def stop(self):
        """
        Stop the node.
        """

        # stop the HTTP server
        self.http_server.shutdown()


def main():
    """
    Run the bridge node daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help="bind to IP address or hostname")
    parser.add_argument('--port', type=int, default=5510, help="HTTP API port")
    parser.add_argument('--daemon', action='store_true', help="run as daemon in background")

    args = parser.parse_args()

    # create the bridge node
    node = BridgeNode(host=args.host, port=args.port)

    # create the daemon context
    context = daemon.DaemonContext(
        files_preserve=[node.http_socket.fileno()],
        signal_map={signal.SIGTERM: node.stop})

    if not args.daemon:
        # run the process in the foreground
        context.detach_process = False

        # preserve standard file descriptors
        context.stdin = sys.stdin
        context.stdout = sys.stdout
        context.stderr = sys.stderr

    # run the daemon
    with context:
        node.run()
