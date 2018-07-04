from http import HTTPStatus

from mdcs.http.view import View
from mdcs.schema import DeviceSchema, AttributeSchema, ActionSchema

from mdcs_node.generic.schema import NodeSchema


class NodeDetail(View):
    def get(self, request, config, node):
        schema = NodeSchema()
        return schema.dump(node).data


class NodeHealth(View):
    def get(self, request, config, node):
        # TODO: implement this (compatible with HAProxy)
        return HTTPStatus.OK


class DeviceList(View):
    def get(self, request, config, node):
        schema = DeviceSchema(many=True)
        return schema.dump(node.devices.values()).data


class DeviceDetail(View):
    def get(self, request, config, node, device):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        schema = DeviceSchema()
        return schema.dump(node.devices[device]).data


class AttributeDetail(View):
    def get(self, request, config, node, device, path):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        device = node.devices[device]
        if path not in device.attributes:
            return (HTTPStatus.NOT_FOUND, "attribute not found")

        schema = AttributeSchema()
        return schema.dump(device.attributes[path]).data


class AttributeValue(View):
    def get(self, request, config, node, device, path):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        device = node.devices[device]
        if path not in device.attributes:
            return (HTTPStatus.NOT_FOUND, "attribute not found")

        attribute = device.attributes[path]
        if not attribute.readable:
            return (HTTPStatus.BAD_REQUEST, "attribute cannot be read")

        # TODO: encode this to JSON using Avro?
        return attribute.read()

    def put(self, request, config, node, device, path):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        device = node.devices[device]
        if path not in device.attributes:
            return (HTTPStatus.NOT_FOUND, "attribute not found")

        attribute = device.attributes[path]
        if not attribute.writable:
            return (HTTPStatus.BAD_REQUEST, "attribute cannot be modified")

        # TODO: decode this from JSON using Avro?
        attribute.write(request.json)
        return HTTPStatus.NO_CONTENT


class ActionDetail(View):
    def get(self, request, config, node, device, path):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        device = node.devices[device]
        if path not in device.actions:
            return (HTTPStatus.NOT_FOUND, "action not found")

        schema = ActionSchema()
        return schema.dump(device.actions[path]).data


class ActionRun(View):
    def post(self, request, config, node, device, path):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        device = node.devices[device]
        if path not in device.actions:
            return (HTTPStatus.NOT_FOUND, "action not found")

        action = device.actions[path]

        # TODO: implement this
        return HTTPStatus.FORBIDDEN
