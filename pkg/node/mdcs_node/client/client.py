from urllib.parse import urljoin
from http import HTTPStatus

import requests

from mdcs.schema import DeviceSchema

from mdcs_node.schema import NodeSchema
from .device import RemoteDevice


class NodeClient:
    """
    A client for remote Nodes.
    """

    def __init__(self, host, http_port):
        self._host = host
        self._http_port = http_port

        # retrieve the Node name and configuration settings
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

    @property
    def node_http_api(self):
        return "http://{0}:{1}/".format(self._host, self._http_port)

    def _get_node_data(self):
        response = requests.get(self.node_http_api)
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error retrieving node data: {0}".format(response))

        node, errors = NodeSchema().load(response.json())
        if errors:
            raise RuntimeError("failed to parse node data: {0}".format(errors))

        return node

    def get_devices(self):
        response = requests.get(urljoin(self.node_http_api, "d"))
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error retrieving device data from node: {0}".format(response))

        devices, errors = DeviceSchema().load(response.json(), many=True)
        if errors:
            raise RuntimeError("failed to parse device data: {0}".format(errors))

        return [RemoteDevice(self, device) for device in devices]

    def get_device(self, name):
        response = requests.get(urljoin(self.node_http_api, "d/{0}".format(name)))
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error retrieving device data from node: {0}".format(response))

        device, errors = DeviceSchema().load(response.json())
        if errors:
            raise RuntimeError("failed to parse device data: {0}".format(errors))

        return RemoteDevice(self, device)
