from marshmallow import Schema
from marshmallow.fields import String
from marshmallow.validate import Length


class ColorControl(Schema):
    """
    Serialization schema for ColorControl model instances.
    """

    uuid = String(dump_only=True)
    control_uuid = String(dump_only=True)
