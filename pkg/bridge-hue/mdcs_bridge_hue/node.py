#!/usr/bin/env python

import uuid


class Node:
    """
    A control system node.
    """

    def __init__(self):
        """
        Create a new node.
        """

        # create a unique identifier
        self.uuid = uuid.uuid4()

        # keep track of connected devices
        self.devices = {}

    def add_device(self, device):
        """
        Add a device to this node.
        """

        if device.uuid in self.devices:
            raise KeyError("device {0} already exists".format(device))

        self.devices[device.uuid] = device

    def remove_device(self, device):
        """
        Remove a device from this node.
        """

        if not device.uuid in self.devices:
            raise KeyError("device {0} not found".format(device))

        del self.devices[device.uuid]
