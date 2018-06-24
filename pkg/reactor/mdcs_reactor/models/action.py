from sqlalchemy import Column, Integer, String, Text
from marshmallow import Schema, fields, validate

from .base import ModelBase


class Action(ModelBase):
    """
    Database model for a runnable action.
    """

    __tablename__ = 'action'

    uuid = Column(String(22), primary_key=True)
    title = Column(String(64), unique=True)
    content = Column(Text)

    def __repr__(self):
        return "<Action(title='{0}', content='{1}')>".format(self.title, self.content)


class ActionSchema(Schema):
    """
    Serialization schema for a runnable action.
    """

    uuid = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=64))
    content = fields.String(required=True, validate=validate.Length(min=1))
