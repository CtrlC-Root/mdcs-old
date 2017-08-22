import socket

import psutil

from mdcs.generic import Device, AttributeFlags, DelegatedAttribute


class HostDevice(Device):
    """
    A device for the local host.
    """

    def __init__(self):
        super().__init__("host-{0}".format(socket.gethostname()), {})

        # create attributes and actions
        self.add_attribute(DelegatedAttribute(
            'hostname',
            AttributeFlags.READ,
            'string',
            self.read_hostname,
            None))

        self.add_attribute(DelegatedAttribute(
            'cpu.count',
            AttributeFlags.READ,
            'int',
            self.read_cpu_count,
            None))

        self.add_attribute(DelegatedAttribute(
            'cpu.usage',
            AttributeFlags.READ,
            {
                'type': 'array',
                'items': {
                    'type': 'record',
                    'fields': [
                        {'name': 'user', 'type': 'float'},
                        {'name': 'system', 'type': 'float'},
                        {'name': 'idle', 'type': 'float'}
                    ]
                }
            },
            self.read_cpu_usage,
            None))

        self.add_attribute(DelegatedAttribute(
            'memory.total',
            AttributeFlags.READ,
            'int',
            self.read_memory_total,
            None))

        self.add_attribute(DelegatedAttribute(
            'memory.used',
            AttributeFlags.READ,
            'int',
            self.read_memory_used,
            None))

        self.add_attribute(DelegatedAttribute(
            'memory.free',
            AttributeFlags.READ,
            'int',
            self.read_memory_free,
            None))

    def read_hostname(self):
        return socket.gethostname()

    def read_cpu_count(self):
        return psutil.cpu_count(logical=True)

    def read_cpu_usage(self):
        return map(
            lambda d: {'user': d.user, 'system': d.system, 'idle': d.idle},
            psutil.cpu_times(percpu=True))

    def read_memory_total(self):
        return psutil.virtual_memory().total

    def read_memory_used(self):
        return psutil.virtual_memory().used

    def read_memory_free(self):
        return psutil.virtual_memory().free
