from marshmallow import Schema, pre_dump
from marshmallow.fields import String, DateTime, Dict


class Task(Schema):
    """
    Serialization schema for Task model instances.
    """

    uuid = String(dump_only=True)
    controlset_uuid = String(dump_only=True)
    state = String(dump_only=True)
    created = DateTime(dump_only=True)
    modified = DateTime(dump_only=True)
    input = Dict(dump_only=True)
    output = Dict(dump_only=True)

    @pre_dump
    def jsonify_task(self, task):
        return {
            'uuid': task.uuid,
            'controlset_uuid': task.controlset_uuid,
            'state': task.state.name,
            'created': task.created,
            'modified': task.modified,
            'input': task.input,
            'output': task.output}
