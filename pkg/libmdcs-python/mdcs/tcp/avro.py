import socket
from io import BytesIO

from avro.io import DatumReader, DatumWriter
from avro.ipc import Transceiver, FramedReader, FramedWriter
from avro.datafile import DataFileReader, DataFileWriter


def serialize_value(schema, value):
    """
    Serialize a value to binary using the given Avro schema.
    """

    data_buffer = BytesIO()
    writer = DataFileWriter(data_buffer, DatumWriter(), schema)
    writer.append(value)
    writer.flush()

    return data_buffer.getvalue()


def unserialize_value(schema, data):
    """
    Unserialize a value from binary using the given Avro schema.
    """

    data_buffer = BytesIO(data)
    reader = DataFileReader(data_buffer, DatumReader())
    value = next(reader, None)
    reader.close()

    return value


class TCPTransceiver(Transceiver):
    """
    An Avro IPC transceiver that uses a TCP connection to send and receive messages.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port

        # connect to the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        # create a buffered file for reading from the socket
        self.rfile = self.socket.makefile('rb', -1)

    @property
    def remote_name(self):
        return self.socket.getsockname()

    def ReadMessage(self):
        reader = FramedReader(self.rfile)
        message = reader.Read()

        return message

    def WriteMessage(self, message):
        send_buffer = BytesIO()
        writer = FramedWriter(send_buffer)
        writer.Write(message)

        self.socket.send(send_buffer.getvalue())

    def Close(self):
        self.rfile.close()
        self.socket.close()
