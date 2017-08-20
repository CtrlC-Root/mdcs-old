#!/usr/bin/env python

from http import HTTPStatus

from mdcs.generic.attribute import AttributeFlags


def attribute_detail(node, method, args):
    if method != 'GET':
        return (HTTPStatus.METHOD_NOT_ALLOWED, '')

    if args['device'] not in node.devices:
        return (HTTPStatus.NOT_FOUND, 'device not found')

    device = node.devices[args['device']]
    if args['path'] not in device.attributes:
        return (HTTPStatus.NOT_FOUND, 'attribute not found')

    return device.attributes[args['path']]


def attribute_value(node, method, args):
    if args['device'] not in node.devices:
        return (HTTPStatus.NOT_FOUND, 'device not found')

    device = node.devices[args['device']]
    if args['path'] not in device.attributes:
        return (HTTPStatus.NOT_FOUND, 'attribute not found')

    attribute = device.attributes[args['path']]
    if method == 'GET':
        if not attribute.readable:
            raise RuntimeError("attribute value can not be read")

        return attribute.read()

    if not attribute.writable:
        raise RuntimeError("attribute value can not be modified")

    # TODO: write attribute value
    pass
