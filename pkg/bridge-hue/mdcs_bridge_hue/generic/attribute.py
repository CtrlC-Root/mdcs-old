#!/usr/bin/env python

from enum import IntFlag


class AttributeFlags(IntFlag):
    """
    Attribute flags that represent capabilities and allowed usage.
    """

    DYNAMIC = 1     # can be added and removed at runtime
    READ = 2        # clients can read value
    WRITE = 4       # clients can write value


class Attribute:
    """
    An attribute that represents part of a device's current state.
    """

    def __init__(self, path, flags):
        self.path = path
        self.flags = flags

    @property
    def dynamic(self):
        return AttributeFlags.DYNAMIC in self.flags

    @property
    def readable(self):
        return AttributeFlags.READ in self.flags

    @property
    def writable(self):
        return AttributeFlags.WRITE in self.flags

    def read(self):
        """
        Read the attribute value.
        """

        raise NotImplemented()

    def write(self, value):
        """
        Write the attribute value.
        """

        raise NotImplemented()
