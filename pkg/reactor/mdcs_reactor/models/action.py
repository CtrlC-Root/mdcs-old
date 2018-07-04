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

    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#one-to-many
    # http://docs.sqlalchemy.org/en/latest/orm/cascades.html
    tasks = relationship(
        'Task',
        order_by='Task.uuid',
        cascade='save-update, merge, delete, delete-orphan',
        cascade_backrefs=False,
        back_populates='action')

    def __repr__(self):
        return "<Action(uuid='{0}', title='{1}', content='{2}')>".format(
            self.uuid,
            self.title,
            self.content)
