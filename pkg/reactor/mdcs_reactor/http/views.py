from http import HTTPStatus

import shortuuid
from mdcs.http.view import View

from mdcs_reactor.models import Action


class ReactorDetail(View):
    def get(self, request, config, session):
        return {'config': config.to_json()}


class ReactorHealth(View):
    def get(self, request, config, session):
        # TODO: implement this (compatible with HAProxy)
        return HTTPStatus.OK


class ActionList(View):
    def get(self, request, config, session):
        # return a list of all actions in JSON format
        return list(map(lambda a: a.to_json(), session.query(Action).all()))

    def post(self, request, config, session):
        # create the action
        action = Action.from_json(request.json)
        action.uuid = shortuuid.uuid()

        # save it to the database
        session.add(action)
        session.commit()

        # return the newly created action in JSON format
        return action.to_json()
