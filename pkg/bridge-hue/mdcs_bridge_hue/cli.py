#!/usr/bin/env python

import sys
import daemon
import signal
import lockfile
import argparse

from .generic import Node, Device, Attribute, AttributeFlags, Action
from .daemon import NodeServer


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

    # XXX create the bridge node
    device = Device()
    device.add_attribute(Attribute("color.red", AttributeFlags.READ | AttributeFlags.WRITE))
    device.add_attribute(Attribute("color.green", AttributeFlags.READ | AttributeFlags.WRITE))
    device.add_attribute(Attribute("color.blue", AttributeFlags.READ | AttributeFlags.WRITE))
    device.add_attribute(Attribute("brightness", AttributeFlags.READ | AttributeFlags.WRITE))
    device.add_action(Action("blink"))

    node = Node()
    node.add_device(device)

    # create the node server
    server = NodeServer(node=node, http_host=args.host, http_port=args.port)

    # create the daemon context
    def handle_signal(signal_number, stack_frame):
        server.stop()

    context = daemon.DaemonContext(
        files_preserve=[server.http_socket.fileno()],
        signal_map={
            signal.SIGTERM: handle_signal,
            signal.SIGINT: handle_signal})

    if not args.daemon:
        # run the process in the foreground
        context.detach_process = False

        # preserve standard file descriptors
        context.stdin = sys.stdin
        context.stdout = sys.stdout
        context.stderr = sys.stderr

    # run the server
    with context:
        try:
            server.run()

        except KeyboardInterrupt:
            # TODO: log this
            print("received SIGINT, quitting")
