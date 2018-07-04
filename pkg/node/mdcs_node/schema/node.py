from marshmallow import Schema
from marshmallow.fields import String, Nested

from .config import NodeConfigSchema


class NodeSchema(Schema):
    """
    Serialization schema for a Node.
    """

    name = String()
    config = Nested(NodeConfigSchema)
