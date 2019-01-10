import shortuuid
from flask import g, request, jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from mdcs_remote.web import application
from mdcs_remote.models import ControlSet, ControlType, Task
from mdcs_remote.schema import ControlSet as ControlSetSchema
from mdcs_remote.schema import Task as TaskSchema
from mdcs_remote.schema import ButtonValue as ButtonValueSchema
from mdcs_remote.schema import ColorValue as ColorValueSchema


class ControlSetList(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ControlSetSchema()

    def get(self):
        return jsonify(self.schema.dump(g.db.query(ControlSet).all(), many=True).data)

    def post(self):
        # create the control set
        controlset_data, errors = self.schema.load(request.json)
        if errors:
            return jsonify(errors), 400

        controlset = ControlSet(**controlset_data)
        controlset.uuid = shortuuid.uuid()

        # save it to the database
        g.db.add(controlset)
        g.db.commit()

        # return the newly created instance
        return jsonify(self.schema.dump(controlset).data)


class ControlSetDetail(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ControlSetSchema()

    def dispatch_request(self, uuid):
        try:
            controlset = g.db.query(ControlSet).filter(ControlSet.uuid == uuid).one()

        except NoResultFound:
            return 'control set does not exist', 404

        except MultipleResultsFound:
            return 'multiple results found', 500

        return super().dispatch_request(controlset)

    def get(self, controlset):
        return jsonify(self.schema.dump(controlset).data)

    def put(self, controlset):
        updates, errors = self.schema.load(request.json, partial=True)
        if errors:
            return jsonify(errors), 400

        for field, value in updates.items():
            setattr(controlset, field, value)

        g.db.add(controlset)
        g.db.commit()

        return jsonify(self.schema.dump(controlset).data)

    def delete(self, controlset):
        g.db.delete(controlset)
        g.db.commit()

        return 'OK', 200


class ControlSetApply(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_schema = TaskSchema()
        self.button_schema = ButtonValueSchema()
        self.color_schema = ColorValueSchema()

    def dispatch_request(self, uuid):
        try:
            controlset = g.db.query(ControlSet).filter(ControlSet.uuid == uuid).one()

        except NoResultFound:
            return 'control set does not exist', 404

        except MultipleResultsFound:
            return 'multiple results found', 500

        return super().dispatch_request(controlset)

    def post(self, controlset):
        # parse control values
        input_data = {}
        for control in controlset.controls:
            # verify we received value data for this control
            if control.name not in request.json:
                return jsonify({control.name: ["Missing control value data."]}), 400

            # determine which value schema to use
            if control.type == ControlType.BUTTON:
                schema = self.button_schema

            elif control.type == ControlType.COLOR:
                schema = self.color_schema

            else:
                return "internal server error", 500

            # parse the value data
            input_data[control.name], errors = schema.load(request.json[control.name])
            if errors:
                return jsonify({control.name: errors}), 400

            # store the control type with the value data to make parsing
            # easier in the future when the control set may have changed
            input_data[control.name]['type'] = control.type.name

        # create the task
        task = Task(
            uuid=shortuuid.uuid(),
            controlset_uuid=controlset.uuid,
            input=input_data)

        g.db.add(task)
        g.db.commit()

        # enqueue a job for the task in the worker queue
        g.queue.put(task.uuid)

        # return the newly created task
        return jsonify(self.task_schema.dump(task).data)
