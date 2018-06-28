from marshmallow import Schema, post_load, pre_dump
from marshmallow.fields import String, Dict, Nested

from mdcs.generic.device import Device

from .attribute import AttributeSchema
from .action import ActionSchema


class DeviceSchema(Schema):
    """
    Serialization schema for a Device.
    """

    name = String()
    config = Dict()

    attributes = Nested(AttributeSchema, many=True)
    actions = Nested(ActionSchema, many=True)

    @post_load
    def create_device(self, data):
        device = Device(name=data['name'], config=data['config'])

        for attribute in data['attributes']:
            device.add_attribute(attribute)

        for action in data['actions']:
            device.add_action(action)

        return device

    @pre_dump
    def jsonify_device(self, device):
        return {
            'name': device.name,
            'config': device.config,
            'attributes': device.attributes.values(),
            'actions': device.actions.values()}
