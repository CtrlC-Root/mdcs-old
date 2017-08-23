import uuid


class Node:
    """
    A control system node.
    """

    def __init__(self, name=None, config={}):
        """
        Create a new node.
        """

        self._name = name or str(uuid.uuid4())
        self._config = config
        self._devices = {}

    @property
    def name(self):
        return self._name

    @property
    def config(self):
        return self._config

    def update_config(self, config):
        self._config.update(config)

    @property
    def devices(self):
        return self._devices

    def add_device(self, device):
        """
        Add a device to this node.
        """

        if device.name in self._devices:
            raise KeyError("device identifier is not unique")

        self._devices[device.name] = device

    def remove_device(self, device):
        """
        Remove a device from this node.
        """

        if device.name not in self._devices:
            raise KeyError("device not found")

        del self._devices[device.name]
