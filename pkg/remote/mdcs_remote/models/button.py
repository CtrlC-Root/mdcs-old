from sqlalchemy import Column, ForeignKey, String, Enum
from sqlalchemy.orm import relationship

from .control import Control, ControlType


class ButtonControl(Control):
    """
    A button control.
    """

    __tablename__ = 'button_control'
    __mapper_args__ = {
        'polymorphic_identity': ControlType.BUTTON,
    }

    uuid = Column(String(22), ForeignKey('control.uuid'), primary_key=True)
    title = Column(String(16), nullable=False)

    def __repr__(self):
        return "<Button(uuid='{0}', title='{1}')>".format(
            self.uuid,
            self.title)
