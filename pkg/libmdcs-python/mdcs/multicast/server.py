import struct
import socket
from io import BytesIO
from socketserver import UDPServer, DatagramRequestHandler


class NodeMulticastRequestHandler(DatagramRequestHandler):
    def handle(self):
        # TODO: implement this
        print("multicast data from: {0}".format(self.client_address))
        self.wfile.write("ack".encode('utf-8'))


class NodeMulticastServer(UDPServer):
    """
    A server that provides the TCP API for interacting with a Node.
    """

    def __init__(self, node, host, port, group):
        super().__init__((host, port), NodeMulticastRequestHandler, bind_and_activate=False)
        self.allow_reuse_address = True # XXX should be an option?
        self._group = group

        # create the group membership request
        self._group_member = struct.pack('4sL', socket.inet_aton(self._group), socket.INADDR_ANY)

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

    @property
    def group(self):
        return self._group

    def run(self):
        # XXX: why does self.server_bind() fail???
        ## import pdb; pdb.set_trace()

        try:
            # bind and activate the server
            self.server_bind()
            self.server_activate()

        except:
            # close the server
            self.server_close()

            # propagate the error
            raise

        try:
            # join the multicast group
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self._group_member)

            # process requests until stopped
            self.serve_forever()

        finally:
            # leave the multicast group
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, self._group_member)

            # close the server
            self.server_close()
