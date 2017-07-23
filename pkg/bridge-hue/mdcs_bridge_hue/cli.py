#!/usr/bin/env python

import sys
import daemon
import signal
import lockfile
import argparse

from mdcs.generic import Node, Device, Attribute, AttributeFlags, Action
from mdcs.daemon import NodeServer


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

    rw_flags = AttributeFlags.READ | AttributeFlags.WRITE
    device.add_attribute(Attribute("color.red", rw_flags, {'type': 'integer'}))
    device.add_attribute(Attribute("color.green", rw_flags, {'type': 'integer'}))
    device.add_attribute(Attribute("color.blue", rw_flags, {'type': 'integer'}))
    device.add_attribute(Attribute("brightness", rw_flags, {'type': 'integer'}))
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
        server.run()
