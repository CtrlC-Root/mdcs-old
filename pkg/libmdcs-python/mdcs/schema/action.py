import json

from marshmallow import Schema, post_load, pre_dump
from marshmallow.fields import String
from marshmallow.validate import Length

from mdcs.device import Action


class ActionSchema(Schema):
    """
    Serialization schema for a device Action.
    """

    path = String(validate=Length(min=1))
    input_schema = String(validate=Length(min=1))  # XXX: JSON field instead?
    output_schema = String(validate=Length(min=1))  # XXX: JSON field instead?

    @post_load
    def create_action(self, data):
        return Action(
            path=data['path'],
            input_schema=json.loads(data['input_schema']),
            output_schema=json.loads(data['output_schema']))

    @pre_dump
    def jsonify_action(self, action):
        return {
            'path': action.path,
            'input_schema': json.dumps(action.input_schema.to_json()),
            'output_schema': json.dumps(action.output_schema.to_json())}
