#!/usr/bin/env python

import sys
import json
import argparse
from http import HTTPStatus
from datetime import datetime

import requests
import avro.ipc
import avro.schema

from mdcs.tcp import API_PROTOCOL, TCPTransceiver
from mdcs.tcp.avro import serialize_value, unserialize_value


def list_devices(args):
    """
    List available devices.
    """

    # retrieve devices
    response = requests.get("http://{host}:{http_port}/d".format(**vars(args)))
    if response.status_code != HTTPStatus.OK:
        print("error retrieving devices from bridge: {0}".format(response))
        sys.exit(1)

    devices = response.json()

    # display device names
    for device in devices:
        print(device['name'])


def show_device(args):
    """
    Show device attributes and actions.
    """

    # retrieve devices
    response = requests.get("http://{host}:{http_port}/d/{device}".format(**vars(args)))
    if response.status_code != HTTPStatus.OK:
        print("error retrieving device information from bridge: {0}".format(response))
        sys.exit(1)

    device = response.json()

    # display attributes
    for attribute in device['attributes']:
        print("Attribute:", attribute['path'])

    # display actions
    for action in device['actions']:
        print("Action:   ", action['path'])


def read_attribute(args):
    """
    Read an attribute value.
    """

    # retrieve the attribute schema
    response = requests.get("http://{host}:{http_port}/d/{device}/at/{attribute}".format(**vars(args)))
    if response.status_code != HTTPStatus.OK:
        print("error retrieving config from bridge: {0}".format(response))
        sys.exit(1)

    attribute = response.json()
    schema = avro.schema.Parse(json.dumps(attribute['schema']))

    # create the Avro IPC client
    client = TCPTransceiver(args.host, args.tcp_port)
    requestor = avro.ipc.Requestor(API_PROTOCOL, client)

    # read the attribute value
    response = requestor.Request('read', {'target': {'device': args.device, 'attribute': args.attribute}})
    value = unserialize_value(schema, response['value'])
    time = datetime.fromtimestamp(response['time'] / 1000.0)

    # display the value
    print("Time: {0}\nValue: {1}".format(time, value))


def write_attribute(args):
    """
    Write an attribute value.
    """

    # retrieve the attribute schema
    response = requests.get("http://{host}:{http_port}/d/{device}/at/{attribute}".format(**vars(args)))
    if response.status_code != HTTPStatus.OK:
        print("error retrieving config from bridge: {0}".format(response))
        sys.exit(1)

    attribute = response.json()
    schema = avro.schema.Parse(json.dumps(attribute['schema']))

    # create the Avro IPC client
    client = TCPTransceiver(args.host, args.tcp_port)
    requestor = avro.ipc.Requestor(API_PROTOCOL, client)

    # write the attribute value
    response = requestor.Request('write', {
        'target': {'device': args.device, 'attribute': args.attribute},
        'data': {
            'value': serialize_value(schema, json.loads(args.value)),
            'time': int(datetime.now().timestamp() * 1000)
        }
    })

    value = unserialize_value(schema, response['value'])
    time = datetime.fromtimestamp(response['time'] / 1000.0)

    # display the value
    print("Time: {0}\nValue: {1}".format(time, value))


def main():
    """
    Run the console client.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1', help="node hostname or IP address")
    parser.add_argument('--http-port', type=int, default=5510, help="HTTP API port")
    parser.add_argument('--tcp-port', type=int, default=5511, help="TCP API port")
    subparsers = parser.add_subparsers()

    parser_list_devices = subparsers.add_parser('list-devices', description=list_devices.__doc__)
    parser_list_devices.set_defaults(handler=list_devices)

    parser_show_device = subparsers.add_parser('show-device', description=show_device.__doc__)
    parser_show_device.set_defaults(handler=show_device)
    parser_show_device.add_argument('device', type=str, help="device name")

    parser_read = subparsers.add_parser('read', description=read_attribute.__doc__)
    parser_read.set_defaults(handler=read_attribute)
    parser_read.add_argument('device', type=str, help="device name")
    parser_read.add_argument('attribute', type=str, help="attribute name")

    parser_write = subparsers.add_parser('write', description=write_attribute.__doc__)
    parser_write.set_defaults(handler=write_attribute)
    parser_write.add_argument('device', type=str, help="device name")
    parser_write.add_argument('attribute', type=str, help="attribute name")
    parser_write.add_argument('value', type=str, help="JSON encoded value")

    args = parser.parse_args()

    # run the handler
    args.handler(args)
