from collections import namedtuple


class Registry:
    """
    An in-memory index of nodes and devices.
    """

    NodeEntry = namedtuple('NodeEntry', ['name', 'host', 'http_port', 'tcp_port'])
    DeviceEntry = namedtuple('DeviceEntry', ['name', 'node'])

    def __init__(self):
        """
        Create an empty registry
        """

        self.nodes = {}
        self.devices = {}

    def clear(self):
        """
        Remote all nodes and devices.
        """

        self.nodes.clear()
        self.devices.clear()

    def add_node(self, name, host, http_port, tcp_port):
        # set or update the node entry
        self.nodes[name] = self.NodeEntry(name, host, http_port, tcp_port)

    def remove_node(self, name):
        # remove device entries for this node
        for device in list(self.devices.values()):
            if device.node == name:
                del self.devices[device.name]

        # remove node entry
        if name in self.nodes:
            del self.nodes[name]

    def add_device(self, name, node):
        # set or update the device entry
        self.devices[name] = self.DeviceEntry(name, node)

    def remove_device(self, name):
        # remove device entry
        if name in self.devices:
            del self.devices[name]
