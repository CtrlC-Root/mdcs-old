import json

import avro.schema


class Action:
    """
    An action that changes a device's current state.
    """

    def __init__(self, path, input_schema, output_schema):
        self._path = path
        self._input_schema = avro.schema.Parse(json.dumps(input_schema))
        self._output_schema = avro.schema.Parse(json.dumps(output_schema))

    @property
    def path(self):
        return self._path

    @property
    def input_schema(self):
        return self._input_schema

    @property
    def output_schema(self):
        return self._output_schema

    def run(self, input_data):
        """
        Run the action with the given arguments.
        """

        raise NotImplemented()


class DelegatedAction(Action):
    """
    An action that uses an external function to modify the device's current state.
    """

    def __init__(self, path, input_schema, output_schema, handler):
        super().__init__(path, input_schema, output_schema)
        self._handler = handler

    def run(self, input_data):
        return self._handler()
