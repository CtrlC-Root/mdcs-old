#!/usr/bin/env python

import uuid
from http import HTTPStatus

from mdcs_bridge_hue.generic.attribute import AttributeFlags


def attribute_detail(node, method, args):
    if method != 'GET':
        return (HTTPStatus.METHOD_NOT_ALLOWED, '')

    try:
        device_uuid = uuid.UUID(hex=args['device'], version=4)

    except Exception as e:
        return (HTTPStatus.INTERNAL_SERVER_ERROR, str(e))

    if device_uuid not in node.devices:
        return (HTTPStatus.NOT_FOUND, 'device not found')

    device = node.devices[device_uuid]
    if args['path'] not in device.attributes:
        return (HTTPStatus.NOT_FOUND, 'attribute not found')

    attribute = device.attributes[args['path']]
    return {
        'device': str(device.uuid),
        'attribute': attribute.path,
        'flags': [flag.name for flag in AttributeFlags if flag in attribute.flags],
        'schema': attribute.schema,
    }
