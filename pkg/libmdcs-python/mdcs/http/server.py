#!/usr/bin/env python

import json
import socket
import inspect
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException

from .json import JSONEncoder
from .node import node_detail, node_health
from .device import device_list, device_detail
from .attribute import attribute_detail, attribute_value
from .action import action_detail


class NodeHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    A handler for node HTTP API requests.
    """

    def do_GET(self):
        """
        TODO.
        """

        # XXX
        try:
            request_url = urllib.parse.urlparse(self.path)
            endpoint, args = self.server.urls.match(
                path_info=request_url.path,
                method=self.command,
                query_args=request_url.query)

        except HTTPException as e:
            # TODO handle different exceptions appropriately
            print(e)
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return

        # retrieve and execute the view
        if endpoint not in self.server.views:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()

            self.wfile.write("endpoint not implemented".encode('utf-8'))
            return

        view = self.server.views[endpoint]
        response = view(self.server.node, self.command, args)

        # process the response
        if isinstance(response, tuple) and len(response) == 2:
            status_code, message = response

            self.send_response(status_code)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()

            self.wfile.write(message.encode('utf-8'))
            return

        try:
            # encode to JSON
            json_value = JSONEncoder().encode(response)

        except:
            # TODO handle different exceptions appropriately
            print(e)
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return

        # send the JSON data
        self.send_response(HTTPStatus.OK)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/javascript')
        self.end_headers()

        self.wfile.write(json_value.encode('utf-8'))


class NodeHTTPServer(HTTPServer):
    """
    A server that provides the HTTP API for interacting with a Node.
    """

    def __init__(self, node, host, port):
        super().__init__((host, port), NodeHTTPRequestHandler, bind_and_activate=False)

        # store the server settings
        self.node = node

        # create the views
        self.views = {
            'node_detail': node_detail,
            'node_health': node_health,
            'device_list': device_list,
            'device_detail': device_detail,
            'attribute_detail': attribute_detail,
            'attribute_value': attribute_value,
            'action_detail': action_detail
        }

        # create the URL dispatch rules
        self.urls = None
        self.routes = Map([
            Rule('/', methods=['GET'], endpoint='node_detail'),
            Rule('/health', methods=['GET'], endpoint='node_health'),

            Rule('/devices', methods=['GET'], endpoint='device_list'),
            Rule('/devices/<device>', methods=['GET'], endpoint='device_detail'),
            Rule('/devices/<device>/attributes/<path>', methods=['GET'], endpoint='attribute_detail'),
            Rule('/devices/<device>/attribute/<path>/value', methods=['GET', 'PUT'], endpoint='attribute_value'),
            Rule('/devices/<device>/actions/<path>', methods=['GET'], endpoint='action_detail'),

            Rule('/d', methods=['GET'], endpoint='device_list'),
            Rule('/d/<device>', methods=['GET'], endpoint='device_detail'),
            Rule('/d/<device>/at/<path>', methods=['GET'], endpoint='attribute_detail'),
            Rule('/d/<device>/at/<path>/v', methods=['GET', 'PUT'], endpoint='attribute_value'),
            Rule('/d/<device>/ac/<path>', methods=['GET'], endpoint='action_detail'),
        ])

    @property
    def host(self):
        assert self.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.server_address[0]

    @property
    def port(self):
        assert self.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.server_address[1]

    def run(self):
        try:
            # bind and activate the HTTP server
            self.server_bind()
            self.server_activate()

            # create the route adapter
            self.urls = self.routes.bind(
                server_name='{0}:{1}'.format(self.host, self.port),
                url_scheme='http')

            # process HTTP requests until stopped
            self.serve_forever()

        finally:
            # close the HTTP server
            self.server_close()

            # remove the route adapter
            self.urls = None
