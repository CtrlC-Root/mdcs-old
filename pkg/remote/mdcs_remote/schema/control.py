from marshmallow import Schema, pre_dump, post_load
from marshmallow.fields import String, Nested
from marshmallow.validate import Length, OneOf

from mdcs_remote.models.control import ControlType

from .button import ButtonControl


class Control(Schema):
    """
    Serialization schema for Control model instances.
    """

    uuid = String(dump_only=True)
    controlset_uuid = String()
    type = String(validate=OneOf(choices=[type.name for type in ControlType]))
    description = String(validate=Length(max=64))

    button = Nested(ButtonControl, exclude=('uuid', 'control_uuid'))

    @post_load
    def parse_control(self, data):
        if 'type' in data:
            data['type'] = ControlType[data['type']]

        return data

    @pre_dump
    def jsonify_control(self, control):
        return {
            'uuid': control.uuid,
            'controlset_uuid': control.controlset_uuid,
            'type': control.type.name,
            'description': control.description,
            'button': control.button}
