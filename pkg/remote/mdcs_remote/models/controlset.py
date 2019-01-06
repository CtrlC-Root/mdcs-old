import enum

from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.orm import relationship

from .generic import Model


class ConfigType(enum.Enum):
    JSON = enum.auto()
    LUA = enum.auto()


class ControlSet(Model):
    """
    A set of controls used to manage a collection of devices.
    """

    __tablename__ = 'controlset'

    uuid = Column(String(22), primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    description = Column(String(64), nullable=False, default="")
    config_type = Column(Enum(ConfigType), nullable=False, default=ConfigType.JSON)
    config = Column(Text, nullable=False)

    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#one-to-many
    # http://docs.sqlalchemy.org/en/latest/orm/cascades.html
    controls = relationship(
        'Control',
        order_by='Control.uuid',
        cascade='save-update, merge, delete, delete-orphan',
        cascade_backrefs=False,
        back_populates='controlset')

    def __repr__(self):
        return "<ControlSet(uuid='{0}', name='{1}', description='{2}', config_type='{3}', config='{4}')>".format(
            self.uuid,
            self.name,
            self.description,
            self.config_type.name,
            self.config)
