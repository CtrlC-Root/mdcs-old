from mdcs.device import Device

from .attribute import RemoteAttribute


class RemoteDevice(Device):
    """
    A remote device.
    """

    def __init__(self, client, device):
        super().__init__(name=device.name, config=device.config)

        for attribute in device.attributes.values():
            self.add_attribute(RemoteAttribute(client, device, attribute))

        # TODO: create corresponding RemoteAction(s)
