from marshmallow import Schema
from marshmallow.fields import String, Nested
from marshmallow.validate import Length

from .task import Task


class Action(Schema):
    """
    Serialization schema for a runnable action.
    """

    uuid = String(dump_only=True)
    title = String(required=True, validate=Length(min=1, max=64))
    content = String(required=True, validate=Length(min=1))

    tasks = Nested(Task, many=True, exclude=('action_uuid',), dump_only=True)
