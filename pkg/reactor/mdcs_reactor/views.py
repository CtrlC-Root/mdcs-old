import shortuuid
from flask import g, request, jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .application import application
from .models import Action


class ActionList(MethodView):
    def get(self):
        return jsonify(list(map(lambda a: a.to_json(), g.db.query(Action).all())))

    def post(self):
        # create the action
        action = Action.from_json(request.json)
        action.uuid = shortuuid.uuid()

        # save it to the database
        g.db.add(action)
        g.db.commit()

        # return the newly created action
        return jsonify(action.to_json())


class ActionDetail(MethodView):
    def dispatch_request(self, uuid):
        try:
            action = g.db.query(Action).filter(Action.uuid==uuid).one()

        except NoResultFound:
            return 'action does not exist', 404

        except MultipleResultsFound:
            return 'multiple results found', 500

        return super().dispatch_request(action)

    def get(self, action):
        return jsonify(action.to_json())

    def put(self, action):
        if 'title' in request.json:
            action.title = request.json['title']

        g.db.add(action)
        g.db.commit()

        return jsonify(action.to_json())

    def delete(self, action):
        g.db.delete(action)
        g.db.commit()

        return 'OK', 200
