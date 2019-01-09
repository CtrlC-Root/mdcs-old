from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .control import Control, ControlType


class ColorControl(Control):
    """
    A color wheel control.
    """

    __tablename__ = 'color_control'
    __mapper_args__ = {
        'polymorphic_identity': ControlType.COLOR,
    }

    uuid = Column(String(22), ForeignKey('control.uuid'), primary_key=True)

    def __repr__(self):
        return "<Color(uuid='{0}')>".format(
            self.uuid)
