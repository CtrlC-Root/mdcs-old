#!/usr/bin/env python

# https://pymotw.com/2/socket/multicast.html
# https://en.wikipedia.org/wiki/Multicast_address

import sys
import struct
import socket

multicast_group = '224.0.0.128'
server_address = ('', 5512)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
    print("waiting to receive message")
    data, address = sock.recvfrom(1024)

    print("received {0} bytes from {1}".format(len(data), address))
    print(data.decode('utf-8'))

    print("sending acknowledgement to {0}".format(address))
    sock.sendto('ack'.encode('utf-8'), address)
