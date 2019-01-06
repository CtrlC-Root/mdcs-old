from flask import g, request, jsonify
from flask.views import MethodView

from mdcs_remote.web import application


class Index(MethodView):
    def get(self):
        # XXX: anything to report here?
        return jsonify({'msg': 'mdcs remote'})
