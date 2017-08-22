import socket
from io import BytesIO

from avro.ipc import Transceiver, FramedReader, FramedWriter


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

    @property
    def remote_name(self):
        return self.socket.getsockname()

    def ReadMessage(self):
        recv_data = self.socket.recv(65535) # XXX lol wut
        recv_buffer = BytesIO(recv_data)

        reader = FramedReader(recv_buffer)
        message = reader.Read()

        return message

    def WriteMessage(self, message):
        send_buffer = BytesIO()
        writer = FramedWriter(send_buffer)
        writer.Write(message)

        self.socket.send(send_buffer.getvalue())

    def Close(self):
        self.socket.close()
