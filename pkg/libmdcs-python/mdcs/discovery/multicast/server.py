import struct
import socket
from socketserver import UDPServer, BaseRequestHandler


class NodeMulticastServer(UDPServer):
    """
    A server that provides the Multicast API for interacting with a Node.
    """

    def __init__(self, config, request_handler):
        super().__init__((config.pulic_host, config.port), request_handler, bind_and_activate=False)
        self.allow_reuse_address = True

        # create the group membership request
        self._group_member = struct.pack('4sL', socket.inet_aton(self.group), socket.INADDR_ANY)

    @property
    def host(self):
        assert self.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.server_address[0]

    @property
    def port(self):
        assert self.address_family in [socket.AF_INET, socket.AF_INET6]
        return self.server_address[1]

    def run(self):
        # XXX disable looping multicast traffic back to this machine
        # self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)

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
