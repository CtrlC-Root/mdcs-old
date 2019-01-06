from sqlalchemy import Column, ForeignKey, String, Enum
from sqlalchemy.orm import relationship

from .generic import Model


class ButtonControl(Model):
    """
    A button control.
    """

    __tablename__ = 'button_control'

    uuid = Column(String(22), primary_key=True)
    control_uuid = Column(String(22), ForeignKey('control.uuid'), nullable=False)
    title = Column(String(16), nullable=False)

    control = relationship('Control', back_populates='button')

    def __repr__(self):
        return "<Button(uuid='{0}', control_uuid='{1}', title='{2}')>".format(
            self.uuid,
            self.control_uuid,
            self.title)
