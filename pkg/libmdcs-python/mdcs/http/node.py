#!/usr/bin/env python

import uuid
from http import HTTPStatus


def node_detail(node, method, args):
    # XXX see notes below for health field
    return {'config': node.config, 'health': 'ok'}


def node_health(node, method, args):
    # TODO actually check if we can reach all of our devices?
    # TODO or maybe this should be implementation specific?
    return (HTTPStatus.OK, 'ok')
