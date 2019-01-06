from marshmallow import Schema, pre_dump
from marshmallow.fields import String, Nested
from marshmallow.validate import Length, OneOf

from mdcs_remote.models.controlset import ConfigType

from .control import Control


class ControlSet(Schema):
    """
    Serialization schema for ControlSet model instances.
    """

    uuid = String(dump_only=True)
    name = String(validate=Length(min=1, max=32))
    description = String(validate=Length(max=64))
    config_type = String(validate=OneOf(choices=[type.name for type in ConfigType]))
    config = String(validate=Length(min=1))

    @pre_dump
    def jsonify_task(self, controlset):
        return {
            'uuid': controlset.uuid,
            'name': controlset.name,
            'description': controlset.description,
            'config_type': controlset.config_type.name,
            'config': controlset.config}
