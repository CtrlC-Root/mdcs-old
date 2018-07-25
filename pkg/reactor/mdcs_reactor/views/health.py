from flask import g, request, jsonify
from flask.views import MethodView

from mdcs_reactor.web import application


class Health(MethodView):
    def get(self):
        # TODO: implement this (HAproxy compatible)
        return 'healthy', 200
