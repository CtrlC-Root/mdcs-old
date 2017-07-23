#!/usr/bin/env python

import uuid
from http import HTTPStatus


def action_detail(node, method, args):
    if method != 'GET':
        return (HTTPStatus.METHOD_NOT_ALLOWED, '')

    try:
        device_uuid = uuid.UUID(hex=args['device'], version=4)

    except Exception as e:
        return (HTTPStatus.INTERNAL_SERVER_ERROR, str(e))

    if device_uuid not in node.devices:
        return (HTTPStatus.NOT_FOUND, 'device not found')

    device = node.devices[device_uuid]
    if args['path'] not in device.actions:
        return (HTTPStatus.NOT_FOUND, 'action not found')

    action = device.actions[args['path']]
    return {
        'device': str(device.uuid),
        'action': action.path,
    }
