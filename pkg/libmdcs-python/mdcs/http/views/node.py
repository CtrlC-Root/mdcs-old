from http import HTTPStatus

from mdcs.http.view import View


class NodeDetail(View):
    def get(self, request, config, node):
        return {'name': node.name, 'config': config.json_dict}


class NodeHealth(View):
    def get(self, request, config, node):
        # TODO: implement this (compatible with HAProxy)
        return HTTPStatus.OK
