import uuid


class Device:
    """
    An abstract device composed of configuration settings, current state, and
    actions that can modify that state.
    """

    def __init__(self, name=None, config={}):
        """
        Create a new device.
        """

        # store the device settings
        self.name = name or str(uuid.uuid4())
        self.config = config

        # device state and actions
        self.attributes = {}
        self.actions = {}

    def add_attribute(self, attribute):
        if attribute.path in self.attributes or attribute.path in self.actions:
            raise KeyError("attribute path is not unique")

        self.attributes[attribute.path] = attribute

    def remove_attribute(self, attribute):
        if attribute.path not in self.attributes:
            raise KeyError("attribute not found")

        del self.attributes[attribute.path]

    def add_action(self, action):
        if action.path in self.attributes or action.path in self.actions:
            raise KeyError("action path is not unique")

        self.actions[action.path] = action

    def remove_action(self, action):
        if action.path not in self.actions:
            raise KeyError("action not found")

        self.actions[action.path] = action
