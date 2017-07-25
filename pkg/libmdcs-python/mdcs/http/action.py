#!/usr/bin/env python

import uuid
from http import HTTPStatus


def action_detail(node, method, args):
    if method != 'GET':
        return (HTTPStatus.METHOD_NOT_ALLOWED, '')

    if args['device'] not in node.devices:
        return (HTTPStatus.NOT_FOUND, 'device not found')

    device = node.devices[args['device']]
    if args['path'] not in device.actions:
        return (HTTPStatus.NOT_FOUND, 'action not found')

    action = device.actions[args['path']]
    return {
        'device': device.name,
        'action': action.path,
    }
