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

    def __init__(self, path, flags, schema):
        self.path = path
        self.flags = flags
        self.schema = schema

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


class StoredAttribute(Attribute):
    """
    An attribute that stores its value in memory.
    """

    def __init__(self, path, flags, schema, value):
        super().__init__(path, flags, schema)
        self.value = value

    def read(self):
        return self.value

    def write(self, value):
        self.value = value


class DelegatedAttribute(Attribute):
    """
    An attribute that uses external functions to read and write a value.
    """

    def __init__(self, path, flags, schema, read_handler, write_handler):
        super().__init__(path, flags, schema)
        self.read_handler = read_handler
        self.write_handler = write_handler

    def read(self):
        return self.read_handler()

    def write(self, value):
        return self.write_handler(value)
