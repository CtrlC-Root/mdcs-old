import fnmatch

from mdcs_node import NodeClient

from .device import DeviceProxy


class RegistryProxy:
    """
    A proxy object exposed to Lua scripts that wraps a local Registry object.
    """

    def __init__(self, runtime, registry):
        self._runtime = runtime
        self._registry = registry

    def get_device(self, name):
        """
        Get the device with the given name.
        """

        device_entry = self._registry.devices.get(name, None)
        if device_entry is None:
            raise RuntimeError("device not found in registry: {0}".format(name))

        node = self._registry.nodes[device_entry.node]
        client = NodeClient(name=node.name, host=node.host, http_port=node.http_port, tcp_port=node.tcp_port)
        device = client.get_device(device_entry.name)

        return DeviceProxy(runtime=self._runtime, device=device)

    def get_devices(self, pattern):
        """
        Get a Lua table of devices whose name matches the provided pattern.
        """

        devices = {}
        for device_entry in self._registry.devices.values():
            if not fnmatch.fnmatch(device_entry.name, pattern):
                continue

            node = self._registry.nodes[device_entry.node]
            client = NodeClient(name=node.name, host=node.host, http_port=node.http_port, tcp_port=node.tcp_port)
            device = client.get_device(device_entry.name)

            devices[device.name] = DeviceProxy(
                runtime=self._runtime,
                device=device)

        return self._runtime.table_from(devices)
