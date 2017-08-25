#!/usr/bin/env python

# https://pymotw.com/2/socket/multicast.html

import sys
import struct
import socket

message = "Hello, World!".encode('utf-8')
multicast_group = ('224.0.0.128', 5512)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying to receive data.
sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not go past the local network segment.
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))

try:
    # Send data to the multicast group
    print("sending: {0}".format(message))
    sent = sock.sendto(message, multicast_group)

    # Look for responses from all recipients
    while True:
        print("waiting to receive")

        try:
            data, server = sock.recvfrom(16)

        except socket.timeout:
            print("socket timed out, no more responses")
            break

        else:
            print("received from {0}: {1}".format(server, data))

finally:
    print("closing socket")
    sock.close()
