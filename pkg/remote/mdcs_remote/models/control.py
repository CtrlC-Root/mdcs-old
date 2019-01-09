import enum

from sqlalchemy import Column, ForeignKey, String, Enum
from sqlalchemy.orm import relationship

from .generic import Model


class ControlType(enum.Enum):
    NONE = enum.auto()
    BUTTON = enum.auto()
    COLOR = enum.auto()


class Control(Model):
    """
    A parent table for control set controls. Controls are a complete disjoint specialization.
    """

    __tablename__ = 'control'

    uuid = Column(String(22), primary_key=True)
    controlset_uuid = Column(String(22), ForeignKey('controlset.uuid'), nullable=False)
    type = Column(Enum(ControlType), nullable=False)
    description = Column(String(64), nullable=False, default="")

    controlset = relationship('ControlSet', back_populates='controls')

    __mapper_args__ = {
        'polymorphic_identity': ControlType.NONE,
        'polymorphic_on': type
    }

    def __repr__(self):
        return "<Control(uuid='{0}', controlset_uuid='{1}', type=ControlType.{2}, description='{3}')>".format(
            self.uuid,
            self.controlset_uuid,
            self.type.name,
            self.description)
