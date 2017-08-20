from http import HTTPStatus

from mdcs.http.view import View


class NodeDetail(View):
    def get(self, request):
        return {'name': 'TODO', 'config': {}, 'health': 'TODO'}


class NodeHealth(View):
    def get(self, request):
        return HTTPStatus.OK
