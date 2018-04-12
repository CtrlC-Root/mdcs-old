from http import HTTPStatus

from mdcs.http.view import View


class ReactorDetail(View):
    def get(self, request, config):
        return {'config': config.to_json()}


class ReactorHealth(View):
    def get(self, request, config):
        # TODO: implement this (compatible with HAProxy)
        return HTTPStatus.OK
