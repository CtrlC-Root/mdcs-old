import time

from avro.ipc import Responder
from avro.schema import AvroException

from mdcs.tcp.protocol import API_PROTOCOL
from mdcs.tcp.avro import serialize_value, unserialize_value


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

                # read the value
                value = attribute.read()
                return {'value': serialize_value(attribute.schema, value), 'time': int(round(time.time() * 1000))}

            # check if we can write to the attribute
            if not attribute.writable:
                return {
                    'message': 'attribute is not writable',
                    'device': device.name,
                    'attribute': attribute.path
                }

            # write the value
            data = request['data']['value']
            value = unserialize_value(attribute.schema, data)
            attribute.write(value)

            # XXX client should be able to ask us to re-read the value and return it (set-and-get)
            return {'value': data, 'time': int(round(time.time() * 1000))}

        elif message.name == 'run':
            # TODO: run the action
            return {'message': 'running actions is not implemented'}

        else:
            # unknown message
            raise AvroException("unexpected message: ", msg.name)
