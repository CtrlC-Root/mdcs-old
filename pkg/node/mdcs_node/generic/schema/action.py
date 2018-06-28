from marshmallow import Schema, post_load, pre_dump
from marshmallow.fields import String
from marshmallow.validate import Length

from mdcs.generic.action import Action


class ActionSchema(Schema):
    """
    Serialization schema for a device Action.
    """

    path = String(validate=Length(min=1))
    input_schema = String(validate=Length(min=1))
    output_schema = String(validate=Length(min=1))

    @post_load
    def create_action(self, data):
        return Action(
            path=data['path'],
            input_schema=data['input_schema'],
            output_schema=data['output_schema'])

    @pre_dump
    def jsonify_action(self, action):
        return {
            'path': action.path,
            'input_schema': action.input_schema.to_json(),
            'output_schema': action.output_schema.to_json()}
