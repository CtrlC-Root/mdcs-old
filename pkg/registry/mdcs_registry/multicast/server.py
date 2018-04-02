import struct
import socket
from io import BytesIO
from socketserver import UDPServer, BaseRequestHandler

from avro.io import DatumWriter
from avro.ipc import FramedReader, FramedWriter
from avro.datafile import DataFileWriter

from mdcs.tcp.avro import serialize_value, unserialize_value
from mdcs.multicast.schema import EVENT_SCHEMA


class RegistryMulticastRequestHandler(BaseRequestHandler):
    def setup(self):
        self.registry = self.server.registry
        self.packet, self.socket = self.request

    def handle(self):
        try:
            # parse the event message
            message = unserialize_value(EVENT_SCHEMA, self.packet)

            # check if it's a node event
            if {'node', 'config', 'state'}.issubset(message):
                if message['state'] == 'STARTED':
                    print("adding node {0} with config: {1}".format(message['node'], message['config']))
                    self.registry.add_node(**message['config'], name=message['node'])

                elif message['state'] == 'STOPPED':
                    print("removing node {0}".format(message['node']))
                    self.registry.remove_node(message['node'])

            # check if it's a device event
            elif {'node', 'device', 'state'}.issubset(message):
                if message['state'] == 'CONNECTED':
                    print("adding node {0} device {1}".format(message['node'], message['device']))
                    self.registry.add_device(message['device'], message['node'])

                elif message['state'] == 'DISCONNECTED':
                    print("removing node {0} device {1}".format(message['node'], message['device']))
                    self.registry.remove_device(message['device'])

        except:
            # TODO: log this or something
            pass


class RegistryMulticastServer(UDPServer):
    """
    A server that provides the Multicast API for interacting with the Registry.
    """

    def __init__(self, config, registry):
        super().__init__(
            (config.mcast_host, config.mcast_port),
            RegistryMulticastRequestHandler,
            bind_and_activate=False)

        self.allow_reuse_address = True

        # store the server settings
        self.config = config
        self.registry = registry

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

    def broadcast_event(self, message):
        """
        Send an event message to all members of the multicast group.
        """

        # encode the data into an Avro message
        event_buffer = BytesIO()
        writer = DataFileWriter(event_buffer, DatumWriter(), EVENT_SCHEMA)
        writer.append(message)

        writer.flush()
        event_buffer.seek(0)
        event_data = event_buffer.read()

        # send a multicast message
        self.socket.sendto(event_data, (self.group, self.port))
