from marshmallow import Schema
from marshmallow.fields import String, Integer
from marshmallow.validate import Range


class ColorControl(Schema):
    """
    Serialization schema for color control fields.
    """

    pass


class ColorValue(Schema):
    """
    Serialization schema for color control value.
    """

    red = Integer(required=True, validate=Range(0, 255))
    green = Integer(required=True, validate=Range(0, 255))
    blue = Integer(required=True, validate=Range(0, 255))
