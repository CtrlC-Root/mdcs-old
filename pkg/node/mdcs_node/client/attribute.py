from datetime import datetime

from avro.ipc import Requestor

from mdcs.device import DelegatedAttribute
from mdcs.tcp import API_PROTOCOL, TCPTransceiver
from mdcs.tcp import serialize_value, unserialize_value


class RemoteAttribute(DelegatedAttribute):
    """
    An attribute of a remote device. This will use the TCP API of the remote Node the parent device is connected to
    for reading or writing the value.
    """

    def __init__(self, client, device, attribute):
        """
        Create the remote attribute based on the given client, device, and generic attribute. The client and device
        are necessary to create the read and write messages for the Node TCP API. The attribute is necessary for
        the path, flags, and schema information which is also used to serialize and unserialize values.
        """

        super().__init__(
            path=attribute.path,
            flags=attribute.flags,
            schema=attribute.schema.to_json(),
            read_handler=self._read_remote,
            write_handler=self._write_remote)

        self._client = client
        self._device = device

    def _read_remote(self):
        """
        The base class Attribute.read() method only returns the value while this implementation also returns the
        sample time provided by the TCP API read call. It can be safely ignored if not needed.
        """

        # create the Avro IPC client
        transceiver = TCPTransceiver(self._client.host, self._client.tcp_port)
        requestor = Requestor(API_PROTOCOL, transceiver)

        # read the attribute value
        response = requestor.Request('read', {'target': {'device': self._device.name, 'attribute': self.path}})

        # parse the response
        value = unserialize_value(self.schema, response['value'])
        time = datetime.fromtimestamp(response['time'] / 1000.0)

        return value, time

    def _write_remote(self, value):
        """
        The base class Attribute.write() method only returns the value while this implementation also returns the
        sample time provided by the TCP API write call. It can be safely ignored if not needed.
        """

        # create the Avro IPC client
        transceiver = TCPTransceiver(self._client.host, self._client.tcp_port)
        requestor = Requestor(API_PROTOCOL, transceiver)

        # write the attribute value
        response = requestor.Request('write', {
            'target': {
                'device': self._device.name,
                'attribute': self.path
            },
            'data': {
                'value': serialize_value(self.schema, value),
                'time': int(datetime.now().timestamp() * 1000)
            }
        })

        # parse the response
        value = unserialize_value(self.schema, response['value'])
        time = datetime.fromtimestamp(response['time'] / 1000.0)

        return value, time
