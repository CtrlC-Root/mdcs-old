#!/usr/bin/env python

import sys
import time
import json
import daemon
import signal
import lockfile
import argparse
from http import HTTPStatus

import requests

from mdcs.generic import Node, Device, AttributeFlags, StoredAttribute, Action
from mdcs import NodeServer

from .device import LightDevice


def main():
    """
    Run the bridge node daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help="bind to IP address or hostname")
    parser.add_argument('--http-port', type=int, default=5510, help="HTTP API port")
    parser.add_argument('--tcp-port', type=int, default=5511, help="TCP API port")
    parser.add_argument('--bridge', type=str, required=True, help="bridge hostname or IP address")
    parser.add_argument('--user', type=str, required=True, help="bridge username")
    parser.add_argument('--daemon', action='store_true', help="run as daemon in background")

    args = parser.parse_args()

    # create the bridge node
    node = Node()

    # retrieve available lights from the Hue bridge and create devices
    response = requests.get("http://{0}/api/{1}/lights".format(args.bridge, args.user))
    if response.status_code != HTTPStatus.OK:
        print("error retrieving lights from bridge: {0}".format(response))
        sys.exit(1)

    lights = response.json()
    for light_id, light_data in lights.items():
        name = light_data['uniqueid'][:-3].replace(':', '-')
        print("found light ({0}): {1}".format(light_id, name))
        node.add_device(LightDevice(name, args.bridge, args.user, light_id))

    # create the node server
    server = NodeServer(node=node, host=args.host, http_port=args.http_port, tcp_port=args.tcp_port)

    # create the daemon context
    def handle_signal(signal_number, stack_frame):
        server.stop()

    context = daemon.DaemonContext(
        files_preserve=[server.http_socket.fileno(), server.tcp_socket.fileno()],
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
        print("running...")
        server.start()
        while server.running and server.healthy:
            time.sleep(1)

        if server.running:
            print("server fault, stopping") # XXX: this should be logged
            server.stop()
