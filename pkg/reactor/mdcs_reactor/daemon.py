#!/usr/bin/env python

import sys
import time
import daemon
import signal
import argparse
from http import HTTPStatus

from mdcs.discovery import MulticastDiscoveryConfig
from .server import ReactorServerConfig, ReactorServer


def main():
    """
    Run the reactor daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help="bind to IP address or hostname")
    parser.add_argument('--http-port', type=int, default=5530, help="HTTP API port")
    MulticastDiscoveryConfig.define_args(parser)

    parser.add_argument('--daemon', action='store_true', help="run as daemon in background")

    args = parser.parse_args()

    # create the reactor server
    server_config = ReactorServerConfig(
        public_host=args.host,
        bind_host=args.host,
        http_port=args.http_port,
        discovery=MulticastDiscoveryConfig.from_args(args))

    server = ReactorServer(config=server_config)

    # create the daemon context
    def handle_signal(signal_number, stack_frame):
        server.stop()

    context = daemon.DaemonContext(
        files_preserve=server.files,
        signal_map={
            signal.SIGTERM: handle_signal,
            signal.SIGINT: handle_signal
        })

    if not args.daemon:
        # run the process in the foreground
        context.detach_process = False

        # preserve standard file descriptors
        context.stdin = sys.stdin
        context.stdout = sys.stdout
        context.stderr = sys.stderr

    # run the server
    with context:
        print("running...")
        server.start()
        while server.running and server.healthy:
            time.sleep(1)

        if server.running:
            print("server fault, stopping") # XXX: this should be logged
            server.stop()
