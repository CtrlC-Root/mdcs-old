#!/usr/bin/env python

import io
import socket
import os.path
import argparse

import avro.io
import avro.schema
import avro.datafile
import pkg_resources


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

    # XXX load schemas
    request_schema = avro.schema.Parse(
        pkg_resources.resource_string('mdcs', os.path.join('tcp', 'schema', 'request.json')))

    response_schema = avro.schema.Parse(
        pkg_resources.resource_string('mdcs', os.path.join('tcp', 'schema', 'response.json')))

    # TODO
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((args.host, args.tcp_port))

    # TODO
    request = {'command': {'device': 'hue', 'attribute': 'serial'}}

    # TODO
    request_buffer = io.BytesIO()
    writer = avro.datafile.DataFileWriter(request_buffer, avro.io.DatumWriter(), request_schema)
    writer.append(request)
    writer.flush()

    request_buffer.seek(0)
    request_data = request_buffer.read()
    tcp_socket.send(request_data)
