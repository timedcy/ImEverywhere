#!/usr/bin/env python
# -*- coding:utf8 -*-
import socket
import sys
import time

HOST, PORT = "192.168.4.72", 9999
data = " ".join(sys.argv[1:])

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
for i in range(1, 100):
    sock.sendto(data + "\n", (HOST, PORT))
    received = sock.recv(1024)

    print("Sent:     {}".format(data))
    print("Received: {}".format(received))
	
    time.sleep(1)