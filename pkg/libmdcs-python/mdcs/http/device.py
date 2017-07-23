#!/usr/bin/env python

import uuid
from http import HTTPStatus


def device_list(node, method, args):
    if method != 'GET':
        return (HTTPStatus.METHOD_NOT_ALLOWED, '')

    return {'devices': list(map(str, node.devices.keys()))}


def device_detail(node, method, args):
    if method != 'GET':
        return (HTTPStatus.METHOD_NOT_ALLOWED, '')

    try:
        device_uuid = uuid.UUID(hex=args['device'], version=4)

    except Exception as e:
        return (HTTPStatus.INTERNAL_SERVER_ERROR, str(e))

    if device_uuid not in node.devices:
        return (HTTPStatus.NOT_FOUND, 'device not found')

    device = node.devices[device_uuid]
    return {
        'device': str(device.uuid),
        'attributes': list(map(str, device.attributes.keys())),
        'actions': list(map(str, device.actions.keys())),
    }
