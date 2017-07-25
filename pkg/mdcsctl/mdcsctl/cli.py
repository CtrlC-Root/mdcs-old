#!/usr/bin/env python

import io
import socket
import argparse

import avro.io
import avro.datafile
import pkg_resources

from mdcs.tcp.schema import REQUEST_SCHEMA, RESPONSE_SCHEMA


def main():
    """
    Run the bridge node daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help="node hostname or IP address")
    parser.add_argument('--http-port', type=int, default=5510, help="HTTP API port")
    parser.add_argument('--tcp-port', type=int, default=5511, help="TCP API port")

    args = parser.parse_args()

    # TODO
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((args.host, args.tcp_port))

    # TODO
    request = {'command': {'device': 'hue', 'attribute': 'serial'}}

    # TODO
    request_buffer = io.BytesIO()
    writer = avro.datafile.DataFileWriter(request_buffer, avro.io.DatumWriter(), REQUEST_SCHEMA)
    writer.append(request)
    writer.flush()

    request_buffer.seek(0)
    request_data = request_buffer.read()
    tcp_socket.send(request_data)
