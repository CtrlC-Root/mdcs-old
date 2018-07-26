#!/usr/bin/env python

import argparse
from http import HTTPStatus

import requests

from mdcs.discovery import MulticastDiscoveryConfig
from mdcs.logging import LoggingConfig
from mdcs_node import Node, NodeConfig, NodeDaemon

from .device import LightDevice, GroupDevice


def main():
    """
    Run the bridge node daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help="bind to IP address or hostname")
    parser.add_argument('--http-port', type=int, default=5510, help="HTTP API port")
    parser.add_argument('--tcp-port', type=int, default=5511, help="TCP API port")
    MulticastDiscoveryConfig.define_args(parser)
    LoggingConfig.define_args(parser)

    parser.add_argument('--daemon', action='store_true', help="run as daemon in background")
    parser.add_argument('--bridge', type=str, required=True, help="bridge hostname or IP address")
    parser.add_argument('--user', type=str, required=True, help="bridge username")

    args = parser.parse_args()

    # configure logging
    logging_config = LoggingConfig.from_args(args)
    logging_config.apply()

    # retrieve bridge configuration
    response = requests.get("http://{0}/api/{1}/config".format(args.bridge, args.user))
    if response.status_code != HTTPStatus.OK:
        print("error retrieving config from bridge: {0}".format(response))
        sys.exit(1)

    config = response.json()
    bridge_id = config['bridgeid']

    # create the node
    config = NodeConfig(
        public_host=args.host,
        bind_host=args.host,
        http_port=args.http_port,
        tcp_port=args.tcp_port,
        discovery=MulticastDiscoveryConfig.from_args(args),
        instance={'hueBridge': args.bridge, 'hueUser': args.user})

    node = Node(config=config)

    # retrieve available lights from the Hue bridge and create devices
    response = requests.get("http://{0}/api/{1}/lights".format(args.bridge, args.user))
    if response.status_code != HTTPStatus.OK:
        print("error retrieving lights from bridge: {0}".format(response))
        sys.exit(1)

    lights = response.json()
    for light_id, light_data in lights.items():
        name = "hue-{0}-light-{1}".format(bridge_id, light_id)
        node.add_device(LightDevice(name, args.bridge, args.user, light_id))

    # group 0 always exists
    node.add_device(GroupDevice("hue-{0}-group-0".format(bridge_id), args.bridge, args.user, 0))

    # retrieve available groups from the Hue bridge and create devices
    response = requests.get("http://{0}/api/{1}/groups".format(args.bridge, args.user))
    if response.status_code != HTTPStatus.OK:
        print("error retrieving groups from bridge: {0}".format(response))
        sys.exit(1)

    groups = response.json()
    for group_id, group_data in groups.items():
        name = "hue-{0}-group-{1}".format(bridge_id, group_id)
        node.add_device(GroupDevice(name, args.bridge, args.user, group_id))

    # create the node daemon and run it
    daemon = NodeDaemon(node=node, logging_config=logging_config, background=args.daemon)
    daemon.run()
