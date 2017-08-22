import time
from io import BytesIO
from socketserver import TCPServer, BaseRequestHandler

from avro.ipc import Responder, FramedReader, FramedWriter
from avro.schema import AvroException

from .schema import API_PROTOCOL


class NodeResponder(Responder):
    def __init__(self, node):
        super().__init__(API_PROTOCOL)
        self.node = node

    def Invoke(self, message, request):
        if message.name == 'read' or message.name == 'write':
            target = request['target']

            # retrieve the device
            if target['device'] not in self.node.devices:
                return {'message': 'device not found'}

            device = self.node.devices[target['device']]

            # retrieve the attribute
            if target['attribute'] not in device.attributes:
                return {'message': 'attribute not found'}

            attribute = device.attributes[target['attribute']]

            # check if this is a read
            if message.name == 'read':
                # check if we can read the attribute
                if not attribute.readable:
                    return {
                        'message': 'attribute is not readable',
                        'device': device.name,
                        'attribute': attribute.path
                    }

                # TODO: read the value
                return {'value': bytes([0xDE, 0xAD, 0xBE, 0xEF]), 'time': int(round(time.time() * 1000))}

            # check if we can write to the attribute
            if not attribute.writable:
                return {
                    'message': 'attribute is not writable',
                    'device': device.name,
                    'attribute': attribute.path
                }

            # XXX retrieve the new value
            data = request['data']
            value = data['value']

            # TODO: write the value
            return {'value': bytes([0xDE, 0xAD, 0xBE, 0xEF]), 'time': int(round(time.time() * 1000))}

        elif message.name == 'run':
            # TODO: run the action
            return {'message': 'running actions is not implemented'}

        else:
            # unknown message
            raise AvroException("unexpected message: ", msg.name)


class NodeTCPRequestHandler(BaseRequestHandler):
    def handle(self):
        """
        Process requests from a TCP API client.
        """

        # TODO: modify this to handle multiple consecutive requests instead of one per connection

        # receive the request data
        recv_data = self.request.recv(65535) # XXX lol what
        recv_buffer = BytesIO(recv_data)

        # read the request data
        reader = FramedReader(recv_buffer)
        request_data = reader.Read()

        # process the request
        responder = NodeResponder(self.server.node)
        response_data = responder.Respond(request_data)

        # write the response data
        send_buffer = BytesIO()
        writer = FramedWriter(send_buffer)
        writer.Write(response_data)

        # send the response data
        self.request.send(send_buffer.getvalue())


class NodeTCPServer(TCPServer):
    """
    A server that provides the TCP API for interacting with a Node.
    """

    def __init__(self, node, host, port):
        super().__init__((host, port), NodeTCPRequestHandler, bind_and_activate=False)
        self.allow_reuse_address = True # XXX should be an option?

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
