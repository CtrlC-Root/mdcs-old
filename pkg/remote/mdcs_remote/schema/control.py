from marshmallow import Schema, pre_dump, post_load
from marshmallow.fields import String, Nested
from marshmallow.validate import Length, OneOf, Regexp

from mdcs_remote.models.control import ControlType

from .button import ButtonControl
from .color import ColorControl


class Control(Schema):
    """
    Serialization schema for Control model instances.
    """

    uuid = String(dump_only=True)
    controlset_uuid = String(required=True)
    name = String(required=True, validate=[Length(min=1, max=32), Regexp(r'^[a-zA-Z]([_a-zA-Z0-9]*)$')])
    type = String(required=True, validate=OneOf(choices=[type.name for type in ControlType]))
    description = String(validate=Length(max=64))

    button = Nested(ButtonControl)
    color = Nested(ColorControl)

    @post_load
    def parse_control(self, data):
        if 'type' in data:
            data['type'] = ControlType[data['type']]

        return data

    @pre_dump
    def jsonify_control(self, control):
        data = {
            'uuid': control.uuid,
            'controlset_uuid': control.controlset_uuid,
            'name': control.name,
            'type': control.type.name,
            'description': control.description}

        if control.type == ControlType.BUTTON:
            data['button'] = {'title': control.title}

        elif control.type == ControlType.COLOR:
            data['color'] = {}

        else:
            # TODO: throw specific validation error?
            raise RuntimeError("unknown control type: {0}".format(control.type.name))

        return data
