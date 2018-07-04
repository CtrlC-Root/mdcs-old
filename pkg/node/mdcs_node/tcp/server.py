from io import BytesIO
from socketserver import TCPServer, StreamRequestHandler

from avro.ipc import FramedReader, FramedWriter

from .responder import NodeResponder


class NodeTCPRequestHandler(StreamRequestHandler):
    def handle(self):
        """
        Process requests from a TCP API client.
        """

        # TODO: fix this code to gracefully handle clients that prematurely close (i.e. len(recv_buffer) == 0)
        # TODO: modify this to handle multiple consecutive requests instead of one per connection

        # read the request data
        reader = FramedReader(self.rfile)
        request_data = reader.Read()

        # process the request
        responder = NodeResponder(self.server.node)
        response_data = responder.Respond(request_data)

        # write the response data
        writer = FramedWriter(self.wfile)
        writer.Write(response_data)


class NodeTCPServer(TCPServer):
    """
    A server that provides the TCP API for interacting with a Node.
    """

    def __init__(self, node):
        super().__init__((node.config.tcp_host, node.config.tcp_port), NodeTCPRequestHandler, bind_and_activate=False)
        self.allow_reuse_address = True
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
            # bind and activate the server
            self.server_bind()
            self.server_activate()

            # process requests until stopped
            self.serve_forever()

        finally:
            # close the server
            self.server_close()
