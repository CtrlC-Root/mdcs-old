#!/usr/bin/env python

import daemon
import signal
import lockfile
import argparse


class BridgeNode:
    """
    A bridge node daemon.
    """

    def __init__(self, host, port):
        # HTTP API
        self.host = host
        self.port = port

        # initial run state
        self.running = True

    def handle_sigterm(self):
        """
        Handle a SIGTERM posix signal.
        """

        self.running = False

    def run(self):
        """
        Run the node.
        """

        # XXX: processing loop
        print("Hello, World!")
        while self.running:
            # TODO: do work
            import time
            time.sleep(1)

            print(".",)


def main():
    """
    Run the bridge node daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help="bind to IP address or hostname")
    parser.add_argument('--port', type=int, default=5510, help="HTTP API port")

    args = parser.parse_args()

    # create the bridge node
    node = BridgeNode(host=args.host, port=args.port)

    # create the daemon context
    context = daemon.DaemonContext(
        signal_map = {signal.SIGTERM: node.handle_sigterm})

    # run the daemon
    with context:
        node.run()
