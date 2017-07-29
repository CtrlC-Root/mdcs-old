#!/usr/bin/env python

from http import HTTPStatus


def device_list(node, method, args):
    if method != 'GET':
        return (HTTPStatus.METHOD_NOT_ALLOWED, '')

    return {'devices': list(map(str, node.devices.keys()))}


def device_detail(node, method, args):
    if method != 'GET':
        return (HTTPStatus.METHOD_NOT_ALLOWED, '')

    if args['device'] not in node.devices:
        return (HTTPStatus.NOT_FOUND, 'device not found')

    device = node.devices[args['device']]
    return {
        'device': device.name,
        'attributes': list(device.attributes.keys()),
        'actions': list(device.actions.keys()),
    }
