#!/usr/bin/env python

import argparse

from mdcs.discovery import MulticastDiscoveryConfig

from .generic import Node, NodeDaemonConfig, NodeDaemon
from .device import HostDevice


def main():
    """
    Run the node daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help="bind to IP address or hostname")
    parser.add_argument('--http-port', type=int, default=5510, help="HTTP API port")
    parser.add_argument('--tcp-port', type=int, default=5511, help="TCP API port")
    MulticastDiscoveryConfig.define_args(parser)

    parser.add_argument('--daemon', action='store_true', help="run as daemon in background")

    args = parser.parse_args()

    # create the node
    node = Node()

    # create static devices
    node.add_device(HostDevice())

    # create the node daemon
    config = NodeDaemonConfig(
        public_host=args.host,
        bind_host=args.host,
        http_port=args.http_port,
        tcp_port=args.tcp_port,
        discovery=MulticastDiscoveryConfig.from_args(args),
        background=args.daemon)

    daemon = NodeDaemon(config=config, node=node)

    # run the daemon
    daemon.run()
