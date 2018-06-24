from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

from .base import ModelBase


class Task(ModelBase):
    """
    Database model for a task to run an action.
    """

    __tablename__ = 'task'

    uuid = Column(String(22), primary_key=True)
    action_uuid = Column(String(22), ForeignKey('action.uuid'))
    created = Column(DateTime)

    action = relationship('Action', back_populates='tasks')

    def __repr__(self):
        return "<Task(uuid='{0}', action_uuid='{1}')>".format(
            self.uuid,
            self.action_uuid)


class TaskSchema(Schema):
    """
    Serialization schema for a task to run an action.
    """

    uuid = fields.String(dump_only=True)
    action_uuid = fields.String()
    created = fields.DateTime(dump_only=True)
