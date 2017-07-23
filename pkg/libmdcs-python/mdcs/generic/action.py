#!/usr/bin/env python


class Action:
    """
    An action that changes a device's current state.
    """

    def __init__(self, path):
        self.path = path

    def run(self):
        """
        Run the action with the given arguments.
        """

        raise NotImplemented()
