from marshmallow import Schema, pre_dump, post_load
from marshmallow.fields import String, Nested
from marshmallow.validate import Length, OneOf

from mdcs_remote.models.controlset import ConfigType

from .control import Control


class ControlSet(Schema):
    """
    Serialization schema for ControlSet model instances.
    """

    uuid = String(dump_only=True)
    name = String(required=True, validate=Length(min=1, max=32))
    description = String(validate=Length(max=64))
    config_type = String(validate=OneOf(choices=[type.name for type in ConfigType]))
    config = String(required=True, validate=Length(min=1))

    controls = Nested(Control, many=True, exclude=('controlset_uuid',), dump_only=True)

    @post_load
    def parse_controlset(self, data):
        if 'config_type' in data:
            data['config_type'] = ConfigType[data['config_type']]

        return data

    @pre_dump
    def jsonify_controlset(self, controlset):
        return {
            'uuid': controlset.uuid,
            'name': controlset.name,
            'description': controlset.description,
            'config_type': controlset.config_type.name,
            'config': controlset.config,
            'controls': controlset.controls}
