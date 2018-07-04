import enum
import datetime

from sqlalchemy import Column, ForeignKey, String, DateTime, Enum, Text
from sqlalchemy.orm import relationship

from .generic import Model


class TaskState(enum.Enum):
    PENDING = enum.auto()
    RUNNING = enum.auto()
    CANCELLED = enum.auto()
    COMPLETED = enum.auto()
    FAILED = enum.auto()


class Task(Model):
    """
    Database model for a task to run an action.
    """

    __tablename__ = 'task'

    uuid = Column(String(22), primary_key=True)
    action_uuid = Column(String(22), ForeignKey('action.uuid'), nullable=False)
    state = Column(Enum(TaskState), nullable=False, default=TaskState.PENDING)
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, onupdate=datetime.datetime.now)
    output = Column(Text, nullable=False, default="")

    action = relationship('Action', back_populates='tasks')

    def __repr__(self):
        return "<Task(uuid='{0}', action_uuid='{1}', state='{2}', created={3}, modified={4}, output='{5}')>".format(
            self.uuid,
            self.action_uuid,
            self.state.name,
            self.created,
            self.modified,
            self.output)
