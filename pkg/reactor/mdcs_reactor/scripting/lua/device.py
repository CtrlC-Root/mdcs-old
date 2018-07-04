class DeviceProxy:
    """
    A Lua proxy object that wraps a remote control system device.
    """

    def __init__(self, runtime, device):
        self._runtime = runtime
        self._device = device

    def read(self, path):
        """
        Read an attribute value.
        """

        attribute = self._device.attributes[path]
        return attribute.read()

    def write(self, path, value):
        """
        Write an attribute value.
        """

        attribute = self._device.attributes[path]
        return attribute.write(value)
