import avro.schema


class Action:
    """
    An action that changes a device's current state.
    """

    def __init__(self, path, input_schema, output_schema):
        self.path = path
        self.input_schema = avro.schema.Parse(input_schema)
        self.output_schema = avro.schema.Parse(output_schema)

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
        self.handler = handler

    def run(self, input_data):
        return self.handler()
