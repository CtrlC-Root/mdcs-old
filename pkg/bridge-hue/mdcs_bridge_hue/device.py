#!/usr/bin/env python

import uuid


class Device:
    """
    An abstract device composed of configuration settings, current state, and
    actions that can modify that state.
    """

    def __init__(self):
        """
        Create a new device.
        """

        # create a unique identifier
        self.uuid = uuid.uuid4()
