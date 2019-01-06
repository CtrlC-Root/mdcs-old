from marshmallow import Schema
from marshmallow.fields import String
from marshmallow.validate import Length


class ButtonControl(Schema):
    """
    Serialization schema for Control model instances.
    """

    uuid = String(dump_only=True)
    control_uuid = String(dump_only=True)
    title = String(required=True, validate=Length(min=1, max=16))
