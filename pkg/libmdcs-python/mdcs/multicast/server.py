import time
import struct
import socket
from io import BytesIO
from socketserver import UDPServer, DatagramRequestHandler

from avro.io import DatumWriter
from avro.ipc import FramedReader, FramedWriter
from avro.datafile import DataFileWriter

from .schema import EVENT_SCHEMA


class NodeMulticastRequestHandler(DatagramRequestHandler):
    def handle(self):
        # TODO: anything here?
        pass


class NodeMulticastServer(UDPServer):
    """
    A server that provides the TCP API for interacting with a Node.
    """

    def __init__(self, config, node):
        super().__init__((config.mcast_host, config.mcast_port), NodeMulticastRequestHandler, bind_and_activate=False)
        self.allow_reuse_address = True # XXX should be an option?

        # store the server settings
        self.config = config
        self.node = node

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

    @property
    def group(self):
        return self.config.mcast_group

    def run(self):
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

    def broadcast_event(self, data):
        """
        Send an event to all members of the multicast group.
        """

        # create the event message
        # XXX break out config values as properties on the Node object instead of pulling from dict
        message = {
            'sent': int(round(time.time() * 1000)),
            'node': {
                'name': self.node.name,
                'host': self.config.public_host,
                'http_port': self.config.http_port,
                'tcp_port': self.config.tcp_port
            },
            'data': data
        }

        # encode the data into an Avro message
        event_buffer = BytesIO()
        writer = DataFileWriter(event_buffer, DatumWriter(), EVENT_SCHEMA)
        writer.append(message)

        writer.flush()
        event_buffer.seek(0)
        event_data = event_buffer.read()

        # send a multicast message
        self.socket.sendto(event_data, (self.group, self.port))
