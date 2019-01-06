import shortuuid
from flask import g, request, jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from mdcs_reactor.web import application
from mdcs_reactor.models import ControlSet
from mdcs_reactor.schema import ControlSet as ControlSetSchema


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
