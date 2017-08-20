#!/usr/bin/env python

import io
import time
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
        """
        Process requests from a TCP API client.
        """

        # create the response writer
        response_buffer = io.BytesIO()
        responses = avro.datafile.DataFileWriter(response_buffer, avro.io.DatumWriter(), RESPONSE_SCHEMA)

        # receive the request data and create a reader to unserialize it
        request_data = self.request.recv(65535) # XXX: hard-coded size, what if under or over?
        request_buffer = io.BytesIO(request_data)
        requests = avro.datafile.DataFileReader(request_buffer, avro.io.DatumReader())

        # process requests
        for request in requests:
            try:
                response = self.handle_one_request(request)

            except Exception as e:
                # XXX better way to format this?
                responses.append({'response': {'message': "error: {0}".format(e)}})

            else:
                responses.append({'result': response})

        # close the request reader
        requests.close()

        # retrieve the response data
        responses.flush()
        response_buffer.seek(0)
        response_data = response_buffer.read()

        # send the response data
        self.request.send(response_data)

    def handle_one_request(self, request):
        """
        Process one request and return a response.
        """

        command = request['command']

        # retrieve the relevant device
        if command['device'] not in self.node.devices:
            return {'message': 'device not found', 'device': command['device']}

        device = self.node.devices[command['device']]

        # command is an attribute read or write
        if 'attribute' in command:
            # retrieve the relevant attribute
            if command['attribute'] not in device.attributes:
                return {
                    'message': 'device attribute not found',
                    'device': device.name,
                    'attribute': command['attribute']
                }

            attribute = device.attributes[command['attribute']]

            # parse the attribute value schema
            value_schema = avro.schema.Parse(json.dumps(attribute.schema))

            # write attribute value
            if 'value' in command:
                if not attribute.writable:
                    return {
                        'message': 'device attribute not writable',
                        'device': device.name,
                        'attribute': attribute.path
                    }

                data_buffer = io.BytesIO(command['value'])
                data_reader = avro.datafile.DataFileReader(data_buffer, avro.io.DatumReader())
                value = next(data_reader, None)

                attribute.write(value)
                data_reader.close()

                return {'when': int(round(time.time() * 1000))}

            # read attribute value
            else:
                if not attribute.readable:
                    return {
                        'message': 'device attribute not writable',
                        'device': device.name,
                        'attribute': attribute.path
                    }

                data_buffer = io.BytesIO()
                data_writer = avro.datafile.DataFileWriter(data_buffer, avro.io.DatumWriter(), value_schema)
                data_writer.append(attribute.read())

                data_writer.flush()
                data_buffer.seek(0)
                data = data_buffer.read()
                data_writer.close()

                return {'when': int(round(time.time() * 1000)), 'value': data}

        # command is an action run
        elif 'action' in command:
            # retrieve the relevant action
            if command['action'] not in device.actions:
                return {
                    'message': 'device action not found',
                    'device': device.name,
                    'action': command['action']
                }

            action = device.attributes[command['action']]

            # TODO: parse the action schemas
            # TODO: unserialize input
            # TODO: run action
            # TODO: serialize output

            # XXX temporary hard-coded response
            return {'when': 1200, 'output': bytes([0x0A])}

        # unknown command
        return {'message': 'unknown request'}


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
