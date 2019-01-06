import enum

from sqlalchemy import Column, ForeignKey, String, Enum
from sqlalchemy.orm import relationship

from .generic import Model


class ControlType(enum.Enum):
    BUTTON = enum.auto()


class Control(Model):
    """
    A parent table for control set controls. Controls are a complete disjoint specialization.
    """

    __tablename__ = 'control'

    uuid = Column(String(22), primary_key=True)
    controlset_uuid = Column(String(22), ForeignKey('controlset.uuid'), nullable=False)
    type = Column(Enum(ControlType), nullable=False)
    name = Column(String(16), nullable=False)

    controlset = relationship('ControlSet', back_populates='controls')

    def __repr__(self):
        return "<Control(uuid='{0}', action_uuid='{1}', type='{2}', name={3}')>".format(
            self.uuid,
            self.action_uuid,
            self.type.name,
            self.name)
