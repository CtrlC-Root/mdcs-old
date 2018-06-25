import shortuuid
from flask import g, request, jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from mdcs_reactor.web import application
from mdcs_reactor.models import Action, ActionSchema


class ActionList(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ActionSchema()

    def get(self):
        return jsonify(self.schema.dump(g.db.query(Action).all(), many=True).data)

    def post(self):
        # create the action
        action_data, errors = self.schema.load(request.json)
        if errors:
            return jsonify(errors), 400

        action = Action(**action_data)
        action.uuid = shortuuid.uuid()

        # save it to the database
        g.db.add(action)
        g.db.commit()

        # return the newly created action
        return jsonify(self.schema.dump(action).data)


class ActionDetail(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ActionSchema()

    def dispatch_request(self, uuid):
        try:
            action = g.db.query(Action).filter(Action.uuid == uuid).one()

        except NoResultFound:
            return 'action does not exist', 404

        except MultipleResultsFound:
            return 'multiple results found', 500

        return super().dispatch_request(action)

    def get(self, action):
        return jsonify(self.schema.dump(action).data)

    def put(self, action):
        updates, errors = self.schema.load(request.json, partial=True)
        if errors:
            return jsonify(errors), 400

        for field, value in updates.items():
            setattr(action, field, value)

        g.db.add(action)
        g.db.commit()

        return jsonify(self.schema.dump(action).data)

    def delete(self, action):
        g.db.delete(action)
        g.db.commit()

        return 'OK', 200
