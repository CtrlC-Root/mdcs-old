from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from .generic import Model


class Action(Model):
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
