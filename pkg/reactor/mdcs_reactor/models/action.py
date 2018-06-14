from sqlalchemy import Column, Integer, String

from .base import ModelBase


class Action(ModelBase):
    """
    A runnable action.
    """

    __tablename__ = 'action'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    @staticmethod
    def from_json(data):
        return Action(name=data['name'])

    def to_json(self):
        return {'id': self.id, 'name': self.name}

    def __repr__(self):
        return "<Action(name='{0}')>".format(self.name)
