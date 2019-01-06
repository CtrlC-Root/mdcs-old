from marshmallow import Schema, pre_dump
from marshmallow.fields import String, DateTime


class Task(Schema):
    """
    Serialization schema for a task to run an action.
    """

    uuid = String(dump_only=True)
    action_uuid = String()
    state = String(dump_only=True)
    created = DateTime(dump_only=True)
    modified = DateTime(dump_only=True)
    output = String(dump_only=True)

    @pre_dump
    def jsonify_task(self, task):
        return {
            'uuid': task.uuid,
            'action_uuid': task.action_uuid,
            'state': task.state.name,
            'created': task.created,
            'modified': task.modified,
            'output': task.output}
