from http import HTTPStatus

from mdcs.http.view import View


class RegistryDetail(View):
    def get(self, request, config, registry):
        return {'config': config.json_dict}


class RegistryHealth(View):
    def get(self, request, config, registry):
        # TODO: implement this (compatible with HAProxy)
        return HTTPStatus.OK


class NodeList(View):
    def get(self, request, config, registry):
        # TODO: implement this
        return []


class DeviceList(View):
    def get(self, request, config, registry):
        # TODO: implement this
        return []
