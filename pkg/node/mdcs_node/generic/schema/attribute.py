from marshmallow import Schema, post_load, pre_dump
from marshmallow.fields import String, List, Dict
from marshmallow.validate import Length, ContainsOnly
import avro.schema

from mdcs.generic.attribute import Attribute, AttributeFlags


class AttributeSchema(Schema):
    """
    Serialization schema for a device Attribute.
    """

    path = String(validate=Length(min=1))
    flags = List(String(), validate=ContainsOnly(choices=[flag.name for flag in AttributeFlags]))
    schema = String(validate=Length(min=1))

    @post_load
    def create_attribute(self, data):
        return Attribute(
            path=data['path'],
            flags=[flag for flag in AttributeFlags if flag.name in data['flags']],
            schema=data['schema'])

    @pre_dump
    def jsonify_attribute(self, attribute):
        return {
            'path': attribute.path,
            'flags': [flag.name for flag in AttributeFlags if flag in attribute.flags],
            'schema': attribute.schema.to_json()}
