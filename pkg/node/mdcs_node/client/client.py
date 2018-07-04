import functools
from http import HTTPStatus
from datetime import datetime

import avro.ipc
import requests

from mdcs.device import Device, DelegatedAttribute, DelegatedAction
from mdcs.tcp import API_PROTOCOL, TCPTransceiver
from mdcs.tcp import serialize_value, unserialize_value
from mdcs.schema import DeviceSchema

from mdcs_node.schema import NodeSchema


class NodeClient:
    def __init__(self, host, http_port):
        self._host = host
        self._http_port = http_port

        node_data = self._get_node_data()
        self._node_name = node_data['name']
        self._node_config = node_data['config']

    @property
    def node_name(self):
        return self._node_name

    @property
    def node_config(self):
        return self._node_config

    @property
    def host(self):
        return self._host

    @property
    def http_port(self):
        return self._http_port

    @property
    def tcp_port(self):
        return self._node_config.tcp_port

    def _get_node_data(self):
        response = requests.get("http://{0}:{1}/".format(self._host, self._http_port)) # XXX: use urllib... urljoin
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error retrieving node information: {0}".format(response))

        node, errors = NodeSchema().load(response.json())
        if errors:
            raise RuntimeError("TODO: {0}".format(errors))

        return node

    def _read_attribute(self, device, attribute):
        # create the Avro IPC client
        client = TCPTransceiver(self.host, self.tcp_port)
        requestor = avro.ipc.Requestor(API_PROTOCOL, client)

        # read the attribute value
        response = requestor.Request('read', {'target': {'device': device.name, 'attribute': attribute.path}})
        value = unserialize_value(attribute.schema, response['value'])
        time = datetime.fromtimestamp(response['time'] / 1000.0)

        return value, time

    def _write_attribute(self, device, attribute, value):
        # create the Avro IPC client
        client = TCPTransceiver(self.host, self.tcp_port)
        requestor = avro.ipc.Requestor(API_PROTOCOL, client)

        # write the attribute value
        response = requestor.Request('write', {
            'target': {'device': device.name, 'attribute': attribute.path},
            'data': {
                'value': serialize_value(attribute.schema, value),
                'time': int(datetime.now().timestamp() * 1000)
            }
        })

        value = unserialize_value(attribute.schema, response['value'])
        time = datetime.fromtimestamp(response['time'] / 1000.0)

        return value, time

    def _fix_device(self, device):
        for attribute in list(device.attributes.values()):
            device.attributes[attribute.path] = DelegatedAttribute(
                path=attribute.path,
                flags=attribute.flags,
                schema=attribute.schema.to_json(),
                read_handler=functools.partial(self._read_attribute, device, attribute),
                write_handler=functools.partial(self._write_attribute, device, attribute))

        # TODO: replace Action with DelegatedAction to run actions

    def get_devices(self):
        response = requests.get("http://{0}:{1}/d".format(self._host, self._http_port))
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error retrieving device information from node: {0}".format(response))

        devices, errors = DeviceSchema().load(response.json(), many=True)
        if errors:
            raise RuntimeError("TODO: {0}".format(errors))

        for device in devices:
            self._fix_device(device)

        return devices

    def get_device(self, name):
        response = requests.get("http://{0}:{1}/d/{2}".format(self._host, self._http_port, name))
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error retrieving device information from node: {0}".format(response))

        device, errors = DeviceSchema().load(response.json())
        if errors:
            raise RuntimeError("TODO: {0}".format(errors))

        self._fix_device(device)
        return device
