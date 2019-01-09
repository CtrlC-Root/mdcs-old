from marshmallow import Schema
from marshmallow.fields import String
from marshmallow.validate import Length


class ButtonControl(Schema):
    """
    Serialization schema for ButtonControl model instances.
    """

    title = String(required=True, validate=Length(min=1, max=16))
