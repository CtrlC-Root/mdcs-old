from socketserver import BaseRequestHandler

from mdcs.tcp.avro import unserialize_value

from .schema import EVENT_SCHEMA
from .server import MulticastServer


class SubscribeRequestHandler(BaseRequestHandler):
    def setup(self):
        self.registry = self.server.registry
        self.packet, self.socket = self.request

    def handle(self):
        try:
            # parse the event message
            message = unserialize_value(EVENT_SCHEMA, self.packet)

            # check if it's a node event
            if {'node', 'config', 'event'}.issubset(message):
                if message['event'] == 'ONLINE':
                    print("updating node {0} with config: {1}".format(message['node'], message['config']))
                    self.registry.add_node(**message['config'], name=message['node'])

                elif message['event'] == 'OFFLINE':
                    print("removing node {0}".format(message['node']))
                    self.registry.remove_node(message['node'])

            # check if it's a device event
            elif {'node', 'device', 'event'}.issubset(message):
                if message['event'] == 'ONLINE':
                    print("updating node {0} device {1}".format(message['node'], message['device']))
                    self.registry.add_device(message['device'], message['node'])

                elif message['event'] == 'OFFLINE':
                    print("removing node {0} device {1}".format(message['node'], message['device']))
                    self.registry.remove_device(message['device'])

        except Exception as e:
            # TODO: log this or something
            print('uh oh: {0}'.format(e))


class MulticastSubscribeServer(MulticastServer):
    """
    A multicast network server that fills in the contents of a Registry.
    """

    def __init__(self, config, registry):
        super().__init__(config, SubscribeRequestHandler)
        self.registry = registry
        self._initial_discover = False

    def service_actions(self):
        # send out a discover command when we initially start
        if not self._initial_discover:
            self.send_message({'command': 'DISCOVER'})
            self._initial_discover = True

    def shutdown(self):
        # stop the server
        super().shutdown()

        # clear the initial discover flag
        self._initial_discover = False
