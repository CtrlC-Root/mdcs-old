from marshmallow import Schema
from marshmallow.fields import String, Dict


class NodeSchema(Schema):
    """
    Serialization schema for a Node.
    """

    name = String()
    config = Dict()
