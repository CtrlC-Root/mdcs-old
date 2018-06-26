from marshmallow import Schema
from marshmallow.fields import String, DateTime


class Task(Schema):
    """
    Serialization schema for a task to run an action.
    """

    uuid = String(dump_only=True)
    action_uuid = String()
    created = DateTime(dump_only=True)
