import shortuuid
from flask import g, request, jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from mdcs_remote.web import application
from mdcs_remote.models import Task
from mdcs_remote.schema import Task as TaskSchema


class TaskList(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = TaskSchema()

    def get(self):
        return jsonify(self.schema.dump(g.db.query(Task).all(), many=True).data)


class TaskDetail(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = TaskSchema()

    def dispatch_request(self, uuid):
        try:
            task = g.db.query(Task).filter(Task.uuid == uuid).one()

        except NoResultFound:
            return 'task does not exist', 404

        except MultipleResultsFound:
            return 'multiple results found', 500

        return super().dispatch_request(task)

    def get(self, task):
        return jsonify(self.schema.dump(task).data)
