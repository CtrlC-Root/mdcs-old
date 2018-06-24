from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, validate

from .base import ModelBase
from .task import TaskSchema


class Action(ModelBase):
    """
    Database model for a runnable action.
    """

    __tablename__ = 'action'

    uuid = Column(String(22), primary_key=True)
    title = Column(String(64), unique=True)
    content = Column(Text)

    tasks = relationship('Task', order_by='Task.uuid', back_populates='action')

    def __repr__(self):
        return "<Action(uuid='{0}', title='{1}', content='{2}')>".format(
            self.uuid,
            self.title,
            self.content)


class ActionSchema(Schema):
    """
    Serialization schema for a runnable action.
    """

    uuid = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=64))
    content = fields.String(required=True, validate=validate.Length(min=1))

    tasks = fields.Nested(TaskSchema, many=True, exclude=('action_uuid', ), dump_only=True)
