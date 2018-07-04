import shortuuid
from flask import g, request, jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from mdcs_reactor.web import application
from mdcs_reactor.models import Task
from mdcs_reactor.schema import Task as TaskSchema


class TaskList(MethodView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = TaskSchema()

    def get(self):
        return jsonify(self.schema.dump(g.db.query(Task).all(), many=True).data)

    def post(self):
        # parse the task data
        task_data, errors = self.schema.load(request.json)
        if errors:
            return jsonify(errors), 400

        # create the task
        task = Task(**task_data)
        task.uuid = shortuuid.uuid()

        # save it to the database
        g.db.add(task)
        g.db.commit()

        # create the corresponding job
        g.queue.put(task.uuid)

        # return the newly created task
        return jsonify(self.schema.dump(task).data)


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
