import fnmatch

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

        device = self._registry.devices.get(name, None)
        if device is None:
            raise RuntimeError("device not found in registry: {0}".format(name))

        return DeviceProxy(
            runtime=self._runtime,
            node=self._registry.nodes[device.node],
            device=device)

    def get_devices(self, pattern):
        """
        Get a Lua table of devices whose name matches the provided pattern.
        """

        devices = {}
        for device in self._registry.devices.values():
            if not fnmatch.fnmatch(device.name, pattern):
                continue

            devices[device.name] = DeviceProxy(
                runtime=self._runtime,
                node=self._registry.nodes[device.node],
                device=device)

        return self._runtime.table_from(devices)
