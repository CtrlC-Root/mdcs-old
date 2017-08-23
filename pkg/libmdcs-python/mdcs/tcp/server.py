from io import BytesIO
from socketserver import TCPServer, BaseRequestHandler

from avro.ipc import FramedReader, FramedWriter

from .responder import NodeResponder


class NodeTCPRequestHandler(BaseRequestHandler):
    def handle(self):
        """
        Process requests from a TCP API client.
        """

        # TODO: fix this code to gracefully handle clients that prematurely close (i.e. len(recv_buffer) == 0)
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
