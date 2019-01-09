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
        # create the control
        control_data, errors = self.schema.load(request.json)
        if errors:
            return jsonify(errors), 400

        if control_data['type'] == ControlType.BUTTON:
            if 'button' not in control_data:
                return jsonify({'button': ["Missing data for required field."]}), 400

            button_data = control_data.pop('button')
            control_data.update(button_data)

            control = ButtonControl(**control_data)
            control.uuid = shortuuid.uuid()

        elif control_data['type'] == ControlType.COLOR:
            if 'color' not in control_data:
                return jsonify({'color': ["Missing data for required field."]}), 400

            color_data = control_data.pop('color')
            control_data.update(color_data)

            control = ColorControl(**control_data)
            control.uuid = shortuuid.uuid()

        else:
            return "invalid control type: {0}".format(control.type.name), 400

        g.db.add(control)
        g.db.commit()

        # return the newly created instance
        return jsonify(self.schema.dump(control).data)


class ControlDetail(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ControlSchema()
        self.button_schema = ButtonControlSchema()
        self.color_schema = ColorControlSchema()

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

        # control type can't be changed once it's been created
        updates.pop('type', None)

        # pull out specialized control fields and merge into top-level fields
        button_updates = updates.pop('button', {})
        color_updates = updates.pop('color', {})

        if control.type == ControlType.BUTTON:
            updates.update(button_updates)

        elif control.type == ControlType.COLOR:
            updates.update(color_updates)

        # update and save the model
        for field, value in updates.items():
            setattr(control, field, value)

        g.db.add(control)
        g.db.commit()

        # return the updated instance
        return jsonify(self.schema.dump(control).data)

    def delete(self, control):
        g.db.delete(control)
        g.db.commit()

        return 'OK', 200
