import requests
import fnmatch


class RegistryProxy:
    def __init__(self, registry_url):
        self._url = registry_url
        self._registry = Registry()

    def refresh(self):
        """
        Fetch nodes and devices from the remote registry.
        """

        self._registry = Registry()

        # XXX load nodes
        response = requests.get('{0}/n'.format(self._url))
        if response.status_code != 200:
            raise RuntimeError('failed to retrieve registry nodes: {0}'.format(response))

        for node_name, node_config in response.json().items():
            self._registry.add_node(
                name=node_name,
                host=node_config['host'],
                http_port=node_config['httpPort'],
                tcp_port=node_config['tcpPort'])

        # XXX load devices
        response = requests.get('{0}/d'.format(self._url))
        if response.status_code != 200:
            raise RuntimeError('failed to retrieve registry devices: {0}'.format(response))

        for device_name, device_config in response.json().items():
            self._registry.add_device(
                name=device_name,
                node=device_config['node'])

    def get_devices(self, pattern):
        """
        Get a dictionary of devices whose name matches the provided pattern.
        """

        devices = {}
        for device in self._registry.devices.values():
            if not fnmatch.fnmatch(device.name, pattern):
                continue

            devices[device.name] = DeviceProxy(
                node=self._registry.nodes[device.node],
                device=device)

        return devices
