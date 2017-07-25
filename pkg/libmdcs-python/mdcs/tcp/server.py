#!/usr/bin/env python

import io
import os.path
from socketserver import TCPServer, BaseRequestHandler

import avro.io
import avro.schema
import avro.datafile
import pkg_resources


class NodeTCPRequestHandler(BaseRequestHandler):
    def handle(self):
        request_data = self.request.recv(10240)
        request_buffer = io.BytesIO(request_data)
        reader = avro.datafile.DataFileReader(request_buffer, avro.io.DatumReader())

        for thing in reader:
            print(">> request: ", thing)

        reader.close()


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
        # load and parse the interface schemas
        # TODO: detect path to schema files instead of hard-coding
        self.request_schema = avro.schema.Parse(
            pkg_resources.resource_string('mdcs', os.path.join('tcp', 'schema', 'request.json')))

        self.response_schema = avro.schema.Parse(
            pkg_resources.resource_string('mdcs', os.path.join('tcp', 'schema', 'response.json')))

        try:
            # bind and activate the TCP server
            self.server_bind()
            self.server_activate()

            # process TCP requests until stopped
            self.serve_forever()

        finally:
            # close the TCP server
            self.server_close()
