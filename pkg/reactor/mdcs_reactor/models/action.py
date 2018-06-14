from sqlalchemy import Column, Integer, String

from .base import ModelBase


class Action(ModelBase):
    """
    A runnable action.
    """

    __tablename__ = 'action'

    uuid = Column(String, primary_key=True)
    name = Column(String, unique=True)

    @staticmethod
    def from_json(data):
        action = Action(name=data['name'])
        action.uuid = data.get('uuid', None)

        return action

    def to_json(self):
        return {'uuid': self.uuid, 'name': self.name}

    def __repr__(self):
        return "<Action(name='{0}')>".format(self.name)
