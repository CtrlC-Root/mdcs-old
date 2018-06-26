from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from .generic import Model


class Task(Model):
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
