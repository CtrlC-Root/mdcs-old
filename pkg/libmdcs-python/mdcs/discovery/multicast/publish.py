import logging
from datetime import datetime, timedelta
from socketserver import BaseRequestHandler

from mdcs.tcp.avro import unserialize_value

from .schema import EVENT_SCHEMA
from .server import MulticastServer


class PublishRequestHandler(BaseRequestHandler):
    def setup(self):
        self.logger = logging.getLogger(__name__)

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

        # XXX: catch specific exceptions?
        except Exception as e:
            self.logger.error('multicast publish handler', exc_info=e)


class MulticastPublishServer(MulticastServer):
    """
    A multicast network server that publishes the contents of a Registry.
    """

    def __init__(self, config, registry):
        super().__init__(config, PublishRequestHandler)
        self.registry = registry
        self._publish_timeout = datetime.now()

    def service_actions(self):
        # periodically send out ONLINE states for nodes and devices
        publish_time = datetime.now()
        if publish_time > self._publish_timeout:
            for node in self.registry.nodes.values():
                self.send_message({
                    'node': node.name,
                    'config': {
                        'host': node.host,
                        'http_port': node.http_port,
                        'tcp_port': node.tcp_port
                    },
                    'event': 'ONLINE'
                })

            for device in self.registry.devices.values():
                self.send_message({
                    'node': device.node,
                    'device': device.name,
                    'event': 'ONLINE'
                })

            # XXX this should be a configuration setting
            self._publish_timeout = publish_time + timedelta(seconds=30)

    def shutdown(self):
        # send out OFFLINE messages for nodes
        for node in self.registry.nodes.values():
            self.send_message({
                'node': node.name,
                'config': {
                    'host': node.host,
                    'http_port': node.http_port,
                    'tcp_port': node.tcp_port
                },
                'event': 'OFFLINE'
            })

        # stop the server
        super().shutdown()
