from http import HTTPStatus

from mdcs.http.view import View


class DeviceList(View):
    def get(self, request, node):
        return list(node.devices.values())


class DeviceDetail(View):
    def get(self, request, node, device):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        return node.devices[device]


class AttributeDetail(View):
    def get(self, request, node, device, path):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        device = node.devices[device]
        if path not in device.attributes:
            return (HTTPStatus.NOT_FOUND, "attribute not found")

        return device.attributes[path]


class AttributeValue(View):
    def get(self, request, node, device, path):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        device = node.devices[device]
        if path not in device.attributes:
            return (HTTPStatus.NOT_FOUND, "attribute not found")

        attribute = device.attributes[path]
        if not attribute.readable:
            raise (HTTPStatus.BAD_REQUEST, "attribute cannot be read")

        return attribute.read()


class ActionDetail(View):
    def get(self, request, node, device, path):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        device = node.devices[device]
        if path not in device.actions:
            return (HTTPStatus.NOT_FOUND, "action not found")

        return device.actions[path]


class ActionRun(View):
    def post(self, request, node, device, path):
        if device not in node.devices:
            return (HTTPStatus.NOT_FOUND, "device not found")

        device = node.devices[device]
        if path not in device.actions:
            return (HTTPStatus.NOT_FOUND, "action not found")

        action = device.actions[path]

        # TODO: implement this
        return HTTPStatus.FORBIDDEN
