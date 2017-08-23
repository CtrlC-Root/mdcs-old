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
        self._name = name or str(uuid.uuid4())
        self._config = config

        # device state and actions
        self._attributes = {}
        self._actions = {}

    @property
    def name(self):
        return self._name

    @property
    def config(self):
        return self._config

    @property
    def attributes(self):
        return self._attributes

    def add_attribute(self, attribute):
        if attribute.path in self._attributes or attribute.path in self._actions:
            raise KeyError("attribute path is not unique")

        self._attributes[attribute.path] = attribute

    def remove_attribute(self, attribute):
        if attribute.path not in self._attributes:
            raise KeyError("attribute not found")

        del self._attributes[attribute.path]

    @property
    def actions(self):
        return self._actions

    def add_action(self, action):
        if action.path in self._attributes or action.path in self._actions:
            raise KeyError("action path is not unique")

        self._actions[action.path] = action

    def remove_action(self, action):
        if action.path not in self._actions:
            raise KeyError("action not found")

        self._actions[action.path] = action
