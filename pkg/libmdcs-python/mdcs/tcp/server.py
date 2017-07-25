#!/usr/bin/env python

import io
from socketserver import TCPServer, BaseRequestHandler

import avro.io
import avro.datafile
import pkg_resources

from .schema import REQUEST_SCHEMA, RESPONSE_SCHEMA


class NodeTCPRequestHandler(BaseRequestHandler):
    def handle(self):
        # XXX
        response_buffer = io.BytesIO()
        writer = avro.datafile.DataFileWriter(response_buffer, avro.io.DatumWriter(), RESPONSE_SCHEMA)

        # XXX receive the request
        request_data = self.request.recv(10240)
        request_buffer = io.BytesIO(request_data)
        reader = avro.datafile.DataFileReader(request_buffer, avro.io.DatumReader())

        # XXX process requests
        for thing in reader:
            print(">> request: ", thing)
            writer.append({'result': {'when': 1000, 'value': bytes([0x0A, 0x15])}})

        # XXX
        reader.close()

        # XXX
        writer.flush()
        response_buffer.seek(0)
        response_data = response_buffer.read()

        self.request.send(response_data)


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
        try:
            # bind and activate the TCP server
            self.server_bind()
            self.server_activate()

            # process TCP requests until stopped
            self.serve_forever()

        finally:
            # close the TCP server
            self.server_close()
