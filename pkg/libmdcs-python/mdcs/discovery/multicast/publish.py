from socketserver import BaseRequestHandler

from mdcs.tcp.avro import unserialize_value

from .schema import EVENT_SCHEMA
from .server import MulticastServer


class PublishRequestHandler(BaseRequestHandler):
    def setup(self):
        self.registry = self.server.registry
        self.packet, self.socket = self.request

    def handle(self):
        try:
            # parse the event message
            message = unserialize_value(EVENT_SCHEMA, self.packet)

            # check if it's a command
            if 'command' not in message:
                return

            # process the command
            if message['command'] == 'DISCOVER':
                for node in self.registry.nodes.values():
                    self.server.send_message({
                        'node': node.name,
                        'config': {
                            'host': node.host,
                            'http_port': node.http_port,
                            'tcp_port': node.tcp_port
                        },
                        'event': 'ONLINE'
                    })

                for device in self.registry.devices.values():
                    self.server.send_message({
                        'node': device.node,
                        'device': device.name,
                        'event': 'ONLINE'
                    })

        except e:
            # TODO: log this or something
            print('uh oh: {0}'.format(e))


class MulticastPublishServer(MulticastServer):
    """
    TODO.
    """

    def __init__(self, config, registry):
        super().__init__(config, PublishRequestHandler)
        self.registry = registry
