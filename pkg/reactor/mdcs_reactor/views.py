import shortuuid
from flask import g, request, jsonify
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .application import application
from .models import Action


@application.route('/action/', methods=['GET', 'POST'])
def action_list():
    if request.method == 'GET':
        return jsonify(list(map(lambda a: a.to_json(), g.db.query(Action).all())))

    # create the action
    action = Action.from_json(request.json)
    action.uuid = shortuuid.uuid()

    # save it to the database
    g.db.add(action)
    g.db.commit()

    # return the newly created action
    return jsonify(action.to_json())


@application.route('/action/<action_uuid>', methods=['GET', 'PUT', 'DELETE'])
def action_detail(action_uuid):
    try:
        action = g.db.query(Action).filter(Action.uuid==action_uuid).one()

    except NoResultFound:
        return 'action does not exist', 404

    except MultipleResultsFound:
        return 'multiple results found', 500

    # retrieve the action
    if request.method == 'GET':
        return jsonify(action.to_json())

    # delete the action
    if request.method == 'DELETE':
        g.db.delete(action)
        g.db.commit()

        return 'OK', 200

    # update the action
    if 'title' in request.json:
        action.title = request.json['title']

    # save the action
    g.db.add(action)
    g.db.commit()

    # return the updated action
    return jsonify(action.to_json())
