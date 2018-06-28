class DeviceProxy:
    """
    A Lua proxy object that wraps a remote control system device.
    """

    def __init__(self, runtime, node, device):
        self._runtime = runtime
        self._node = node
        self._device = device

    def read(self, property):
        # TODO
        value = 0
        print("READ {0}.{1}: {2}".format(self._device.name, property, value))
        return value

    def write(self, property, value):
        # TODO
        print("WRITE {0}.{1}: {2}".format(self._device.name, property, value))
