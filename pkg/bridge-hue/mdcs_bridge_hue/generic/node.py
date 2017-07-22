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
            raise KeyError("device identifier is not unique")

        self.devices[device.uuid] = device

    def remove_device(self, device):
        """
        Remove a device from this node.
        """

        if device.uuid not in self.devices:
            raise KeyError("device not found")

        del self.devices[device.uuid]
