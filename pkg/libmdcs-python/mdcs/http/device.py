#!/usr/bin/env python

from http import HTTPStatus


def device_list(node, method, args):
    if method != 'GET':
        return (HTTPStatus.METHOD_NOT_ALLOWED, '')

    return list(node.devices.values())


def device_detail(node, method, args):
    if method != 'GET':
        return (HTTPStatus.METHOD_NOT_ALLOWED, '')

    if args['device'] not in node.devices:
        return (HTTPStatus.NOT_FOUND, 'device not found')

    return node.devices[args['device']]
