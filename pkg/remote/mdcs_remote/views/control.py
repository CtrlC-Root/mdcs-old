import shortuuid
from flask import g, request, jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from mdcs_remote.web import application
from mdcs_remote.models import Control, ControlType, ButtonControl, ColorControl
from mdcs_remote.schema import Control as ControlSchema
from mdcs_remote.schema import ButtonControl as ButtonControlSchema
from mdcs_remote.schema import ColorControl as ColorControlSchema


class ControlList(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ControlSchema()
        self.button_schema = ButtonControlSchema()
        self.color_schema = ColorControlSchema()

    def get(self):
        return jsonify(self.schema.dump(g.db.query(Control).all(), many=True).data)

    def post(self):
        # create the control set
        control_data, errors = self.schema.load(request.json)
        if errors:
            return jsonify(errors), 400

        base_data = control_data.copy()
        base_data.pop('button', None)
        base_data.pop('color', None)

        control = Control(**base_data)
        control.uuid = shortuuid.uuid()

        g.db.add(control)

        # create the specialized control
        if control.type == ControlType.BUTTON:
            button_data, errors = self.button_schema.load(control_data.get('button', {}))
            if errors:
                return jsonify({'button': [errors]}), 400

            button = ButtonControl(**button_data)
            button.uuid = shortuuid.uuid()
            button.control_uuid = control.uuid

            g.db.add(button)

        elif control.type == ControlType.COLOR:
            color_data, errors = self.color_schema.load(control_data.get('color', {}))
            if errors:
                return jsonify({'color': [errors]}), 400

            color = ColorControl(**color_data)
            color.uuid = shortuuid.uuid()
            color.control_uuid = control.uuid

            g.db.add(color)

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
            if field in ['button', 'color']:
                continue

            setattr(control, field, value)

        # specialied control fields
        if control.type == ControlType.BUTTON and 'button' in updates:
            for field, value in updates['button'].items():
                setattr(control.button, field, value)

        elif control.type == ControlType.COLOR and 'color' in updates:
            for field, value in updates['color'].items():
                setattr(control.color, field, value)

        g.db.add(control)
        g.db.commit()

        return jsonify(self.schema.dump(control).data)

    def delete(self, control):
        g.db.delete(control)
        g.db.commit()

        return 'OK', 200