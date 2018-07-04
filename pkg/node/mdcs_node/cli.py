#!/usr/bin/env python

import argparse

from mdcs.discovery import MulticastDiscoveryConfig

from .node import Node, NodeConfig
from .daemon import NodeDaemon
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
    config = NodeConfig(
        public_host=args.host,
        bind_host=args.host,
        http_port=args.http_port,
        tcp_port=args.tcp_port,
        discovery=MulticastDiscoveryConfig.from_args(args))

    node = Node(config=config)

    # create static devices
    node.add_device(HostDevice())

    # create the node daemon and run it
    daemon = NodeDaemon(node=node, background=args.daemon)
    daemon.run()
