#!/usr/bin/env python

import os.path
from socketserver import TCPServer, StreamRequestHandler

import pkg_resources


class NodeTCPRequestHandler(StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip()
        print("{0} wrote: {1}".format(self.client_address[0], self.data))
        self.wfile.write(self.data)


class NodeTCPServer(TCPServer):
    """
    A server that provides the TCP API for interacting with a Node.
    """

    def __init__(self, node, host, port):
        super().__init__((host, port), NodeTCPRequestHandler, bind_and_activate=False)

        # store the server settings
        self.node = node

    @property
    def host(self):
        assert self.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.server_address[0]

    @property
    def port(self):
        assert self.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.server_address[1]

    def run(self):
        # load the API schema definitions
        schema_path = os.path.join('tcp', 'schema') # XXX: detect path to current file in package
        self.request_schema = pkg_resources.resource_string('mdcs', os.path.join(schema_path, 'request.json'))
        self.response_schema = pkg_resources.resource_string('mdcs', os.path.join(schema_path, 'response.json'))

        try:
            # bind and activate the TCP server
            self.server_bind()
            self.server_activate()

            # process TCP requests until stopped
            self.serve_forever()

        finally:
            # close the TCP server
            self.server_close()
