from http import HTTPStatus

import shortuuid
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
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

        # return the newly created action
        return action.to_json()


class ActionDetail(View):
    def get(self, request, config, session, uuid):
        try:
            action = session.query(Action).filter(Action.uuid==uuid).one()

        except NoResultFound:
            return HTTPStatus.NOT_FOUND

        except MultipleResultsFound:
            return HTTPStatus.INTERNAL_SERVER_ERROR

        return action.to_json()

    def put(self, request, config, session, uuid):
        try:
            action = session.query(Action).filter(Action.uuid==uuid).one()

        except NoResultFound:
            return HTTPStatus.NOT_FOUND

        except MultipleResultsFound:
            return HTTPStatus.INTERNAL_SERVER_ERROR

        # update the action
        if 'name' in request.json:
            action.name = request.json['name']

        # save the action
        session.add(action)
        session.commit()

        # return the updated action
        return action.to_json()

    def delete(self, request, config, session, uuid):
        try:
            action = session.query(Action).filter(Action.uuid==uuid).one()

        except NoResultFound:
            return HTTPStatus.NOT_FOUND

        except MultipleResultsFound:
            return HTTPStatus.INTERNAL_SERVER_ERROR

        # delete the action
        session.delete(action)
        session.commit()
