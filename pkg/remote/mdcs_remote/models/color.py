from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .generic import Model


class ColorControl(Model):
    """
    A color wheel control.
    """

    __tablename__ = 'color_control'

    uuid = Column(String(22), primary_key=True)
    control_uuid = Column(String(22), ForeignKey('control.uuid'), nullable=False)

    control = relationship('Control', back_populates='color')

    def __repr__(self):
        return "<Color(uuid='{0}', control_uuid='{1}')>".format(
            self.uuid,
            self.control_uuid)
