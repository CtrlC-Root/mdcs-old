from marshmallow import Schema
from marshmallow.fields import String, Boolean
from marshmallow.validate import Length


class ButtonControl(Schema):
    """
    Serialization schema for button control fields.
    """

    title = String(required=True, validate=Length(min=1, max=16))


class ButtonValue(Schema):
    """
    Serialization schema for button control value.
    """

    clicked = Boolean(required=True)
