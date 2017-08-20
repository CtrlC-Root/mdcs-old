from http import HTTPStatus

from mdcs.http.view import View


class NodeDetail(View):
    def get(self, request):
        node = self.context['node']
        return {'name': node.name, 'config': node.config}


class NodeHealth(View):
    def get(self, request):
        # TODO: implement this (compatible with HAProxy)
        return HTTPStatus.OK
