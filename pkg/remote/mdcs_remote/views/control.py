import shortuuid
from flask import g, request, jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from mdcs_remote.web import application
from mdcs_remote.models import Control, ControlType, ButtonControl
from mdcs_remote.schema import Control as ControlSchema


class ControlList(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ControlSchema()

    def get(self):
        return jsonify(self.schema.dump(g.db.query(Control).all(), many=True).data)

    def post(self):
        # create the control set
        control_data, errors = self.schema.load(request.json)
        if errors:
            return jsonify(errors), 400

        base_data = control_data.copy()
        base_data.pop('button', None)

        control = Control(**base_data)
        control.uuid = shortuuid.uuid()

        g.db.add(control)

        # create the specialized control
        if control.type == ControlType.BUTTON:
            button = ButtonControl(**control_data.get('button', {}))
            button.uuid = shortuuid.uuid()
            button.control_uuid = control.uuid

            g.db.add(button)

        else:
            return "invalid control type: {0}".format(control.type.name), 400

        # save the control objects
        g.db.commit()

        # return the newly created instance
        return jsonify(self.schema.dump(control).data)


class ControlDetail(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ControlSchema()

    def dispatch_request(self, uuid):
        try:
            control = g.db.query(Control).filter(Control.uuid == uuid).one()

        except NoResultFound:
            return 'control does not exist', 404

        except MultipleResultsFound:
            return 'multiple results found', 500

        return super().dispatch_request(control)

    def get(self, control):
        return jsonify(self.schema.dump(control).data)

    def put(self, control):
        updates, errors = self.schema.load(request.json, partial=True)
        if errors:
            return jsonify(errors), 400

        # control fields
        for field, value in updates.items():
            if field in ['button']:
                continue

            setattr(control, field, value)

        # specialied control fields
        if control.type == ControlType.BUTTON and 'button' in updates:
            for field, value in updates['button'].items():
                setattr(control.button, field, value)

            del updates['button']

        g.db.add(control)
        g.db.commit()

        return jsonify(self.schema.dump(control).data)

    def delete(self, control):
        g.db.delete(control)
        g.db.commit()

        return 'OK', 200
