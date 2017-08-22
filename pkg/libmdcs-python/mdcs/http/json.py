import json

from mdcs.generic import Action, Attribute, AttributeFlags, Device

class JSONEncoder(json.JSONEncoder):
    """
    A JSON encoder for control system objects.
    """

    def default(self, obj):
        # encode control system objects
        if isinstance(obj, Action):
            return {
                'path': obj.path,
                'inputSchema': obj.input_schema.to_json(),
                'outputSchema': obj.output_schema.to_json()
            }

        if isinstance(obj, Attribute):
            return {
                'path': obj.path,
                'flags': [flag.name for flag in AttributeFlags if flag in obj.flags],
                'schema': obj.schema.to_json()
            }

        if isinstance(obj, Device):
            return {
                'name': obj.name,
                'actions': list(obj.actions.values()),
                'attributes': list(obj.attributes.values())
            }

        # default implementation
        return super().default(obj)
