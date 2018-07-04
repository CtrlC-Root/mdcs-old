import json
from enum import IntFlag

import avro.schema


class AttributeFlags(IntFlag):
    """
    Attribute flags that represent capabilities and allowed usage.
    """

    READ = 1        # clients can read value
    WRITE = 2       # clients can write value


class Attribute:
    """
    An attribute that represents part of a device's current state.
    """

    def __init__(self, path, flags, schema):
        self._path = path
        self._flags = flags
        self._schema = avro.schema.Parse(json.dumps(schema))

    @property
    def path(self):
        return self._path

    @property
    def flags(self):
        return self._flags

    @property
    def schema(self):
        return self._schema

    @property
    def readable(self):
        return AttributeFlags.READ in self._flags

    @property
    def writable(self):
        return AttributeFlags.WRITE in self._flags

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
        self._read_handler = read_handler
        self._write_handler = write_handler

    def read(self):
        return self._read_handler()

    def write(self, value):
        return self._write_handler(value)
