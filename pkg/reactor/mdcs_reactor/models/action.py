from sqlalchemy import Column, Integer, String, Text

from .base import ModelBase


class Action(ModelBase):
    """
    A runnable action.
    """

    __tablename__ = 'action'

    uuid = Column(String(22), primary_key=True)
    title = Column(String(64), unique=True)
    content = Column(Text)

    @staticmethod
    def from_json(data):
        return Action(
            uuid=data.get('uuid', None),
            title=data.get('title', None),
            content=data.get('content', ''))

    def update(self, data):
        self.title = data.get('title', self.title)
        self.content = data.get('content', self.content)

    def to_json(self):
        return {'uuid': self.uuid, 'title': self.title, 'content': self.content}

    def __repr__(self):
        return "<Action(title='{0}', content='{1}')>".format(self.title, self.content)
