from marshmallow import Schema, pre_dump
from marshmallow.fields import String
from marshmallow.validate import Length, OneOf

from mdcs_remote.models.control import ControlType


class Control(Schema):
    """
    Serialization schema for Control model instances.
    """

    uuid = String(dump_only=True)
    controlset_uuid = String()
    type = String(validate=OneOf(choices=[type.name for type in ControlType]))
    name = String(validate=Length(min=1, max=16))

    @pre_dump
    def jsonify_task(self, control):
        return {
            'uuid': control.uuid,
            'controlset_uuid': control.controlset_uuid,
            'type': control.type.name,
            'name': control.name}
