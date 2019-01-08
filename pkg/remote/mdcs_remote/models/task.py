import enum
from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, DateTime, Enum, Text, JSON
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
    controlset_uuid = Column(String(22), ForeignKey('controlset.uuid'), nullable=False)
    state = Column(Enum(TaskState), nullable=False, default=TaskState.PENDING)
    created = Column(DateTime, nullable=False, default=datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    input = Column(JSON, nullable=False, default={})
    output = Column(JSON, nullable=False, default={})

    controlset = relationship('ControlSet', back_populates='tasks')

    def __repr__(self):
        task_repr = (
            "<Task(uuid='{0}', controlset_uuid='{1}', state=TaskState.{2}, "
            "created={3}, modified={4}, input={5}, output={6})>")

        return task_repr.format(
            self.uuid,
            self.controlset_uuid,
            self.state.name,
            self.created,
            self.modified,
            self.input,
            self.output)
