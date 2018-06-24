from flask import request, jsonify

from .application import application


@application.route('/action/', methods=['GET', 'POST'])
def action_list():
    # TODO: just for testing
    if request.method == 'GET':
        return jsonify([{'uuid': 'foo', 'title': 'Mood Lights'}])

    return jsonify({'uuid': 'bar', 'title': 'Emergency Wipe'})


@application.route('/action/<action_uuid>', methods=['GET', 'PUT', 'DELETE'])
def action_detail(action_uuid):
    # TODO: just for testing
    if request.method == 'GET':
        return jsonify({'uuid': action_uuid, 'title': 'foo'})

    if request.method == 'PUT':
        return jsonify({'uuid': action_uuid, 'title': 'foo'})

    return 'OK', 200
