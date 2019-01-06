from marshmallow import Schema, pre_dump
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

    @pre_dump
    def jsonify_task(self, control):
        return {
            'uuid': control.uuid,
            'controlset_uuid': control.controlset_uuid,
            'type': control.type.name,
            'description': control.description,
            'button': control.button}
