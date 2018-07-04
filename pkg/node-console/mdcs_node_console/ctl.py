#!/usr/bin/env python

import json
import argparse

from beautifultable import BeautifulTable

from mdcs_node.client import NodeClient


def list_devices(client, args):
    """
    List available devices.
    """

    devices = client.get_devices()
    print("\nNode: {0}\n".format(client.node_name))

    table = BeautifulTable()
    table.default_alignment = BeautifulTable.ALIGN_LEFT
    table.column_headers = ["Device"]

    for device in devices:
        table.append_row([device.name])

    print(table)


def show_device(client, args):
    """
    Show device attributes and actions.
    """

    device = client.get_device(args.device)
    print("\nNode: {0}\nDevice: {1}\nConfig: {2}\n".format(
        client.node_name,
        device.name,
        json.dumps(device.config, indent=4, sort_keys=True)))

    attributes = BeautifulTable()
    attributes.default_alignment = BeautifulTable.ALIGN_LEFT
    attributes.column_headers = ["Attribute", "Flags", "Schema"]

    for attribute in device.attributes.values():
        attributes.append_row([
            attribute.path,
            ','.join([flag.name for flag in attribute.flags]),
            attribute.schema.to_json()])

    actions = BeautifulTable()
    actions.default_alignment = BeautifulTable.ALIGN_LEFT
    actions.column_headers = ["Action", "Input", "Output"]

    for action in device.actions.values():
        actions.append_row([
            action.path,
            action.input_schema.to_json(),
            action.output_schema.to_json()])

    print(attributes)
    print(actions)


def read_attribute(client, args):
    """
    Read an attribute value.
    """

    device = client.get_device(args.device)
    print("\nNode: {0}\nDevice: {1}\n".format(
        client.node_name,
        device.name))

    attribute = device.attributes[args.attribute]
    value, time = attribute.read()

    print("Value: {0}\nTime: {1}\n".format(value, time))


def write_attribute(client, args):
    """
    Write an attribute value.
    """

    device = client.get_device(args.device)
    print("\nNode: {0}\nDevice: {1}\n".format(
        client.node_name,
        device.name))

    attribute = device.attributes[args.attribute]
    value, time = attribute.write(json.loads(args.value))

    print("Value: {0}\nTime: {1}\n".format(value, time))


def main():
    """
    Run the console client.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1', help="node hostname or IP address")
    parser.add_argument('--http-port', type=int, default=5510, help="HTTP API port")
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

    # create the node client
    client = NodeClient(host=args.host, http_port=args.http_port)

    # run the command handler
    args.handler(client, args)
