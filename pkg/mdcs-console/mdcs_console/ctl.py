#!/usr/bin/env python

import json
import time
import argparse

import avro.ipc
import avro.schema

from mdcs.tcp import API_PROTOCOL, TCPTransceiver
from mdcs.tcp.avro import serialize_value, unserialize_value


def main():
    """
    Run the console client.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1', help="node hostname or IP address")
    parser.add_argument('--http-port', type=int, default=5510, help="HTTP API port")
    parser.add_argument('--tcp-port', type=int, default=5511, help="TCP API port")

    args = parser.parse_args()

    # XXX serialize attribute value using hard-coded schema
    # XXX ideally we would get this using the HTTP API from the server
    schema = avro.schema.Parse(json.dumps({'type': 'boolean'}))
    value = bool(input('on: ').strip().lower() in ['yes', 'true'])

    # XXX
    client = TCPTransceiver(args.host, args.tcp_port)
    requestor = avro.ipc.Requestor(API_PROTOCOL, client)

    # XXX
    response = requestor.Request('write', {
        'target': {
            'device': 'hue-group-0',
            'attribute': 'on'
        },
        'data': {
            'value': serialize_value(schema, value),
            'time': int(round(time.time() * 1000))
        }
    })

    # XXX
    print(response)
