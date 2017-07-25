#!/usr/bin/env python

import io
import json
from socketserver import TCPServer, BaseRequestHandler

import avro.io
import avro.schema
import avro.datafile
import pkg_resources

from .schema import REQUEST_SCHEMA, RESPONSE_SCHEMA


class NodeTCPRequestHandler(BaseRequestHandler):
    @property
    def node(self):
        return self.server.node

    def handle(self):
        # XXX
        response_buffer = io.BytesIO()
        writer = avro.datafile.DataFileWriter(response_buffer, avro.io.DatumWriter(), RESPONSE_SCHEMA)

        # XXX receive the request
        request_data = self.request.recv(65535)
        request_buffer = io.BytesIO(request_data)
        reader = avro.datafile.DataFileReader(request_buffer, avro.io.DatumReader())

        # XXX process requests
        for request in reader:
            writer.append(self.handle_one_request(request))

        # XXX
        reader.close()

        # XXX
        writer.flush()
        response_buffer.seek(0)
        response_data = response_buffer.read()

        self.request.send(response_data)

    def handle_one_request(self, request):
        """
        Process one request and return a response.
        """

        command = request['command']
        if command['device'] not in self.node.devices:
            return {'result': {'message': 'device not found', 'device': command['device']}}

        device = self.node.devices[command['device']]
        if command['attribute'] not in device.attributes:
            return {'result': {
                'message': 'device attribute not found',
                'device': device.name,
                'attribute': command['attribute']
            }}

        attribute = device.attributes[command['attribute']]
        if 'value' in command:
            # TODO: write value
            return {'result': {'message': 'write not implemented yet'}}

        # XXX
        data_buffer = io.BytesIO()
        value_schema = avro.schema.Parse(json.dumps(attribute.schema))
        data_writer = avro.datafile.DataFileWriter(data_buffer, avro.io.DatumWriter(), value_schema)

        data_writer.append(attribute.read())
        data_writer.flush()
        data_buffer.seek(0)
        data = data_buffer.read()

        return {'result': {'when': 1200, 'value': data}}


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
