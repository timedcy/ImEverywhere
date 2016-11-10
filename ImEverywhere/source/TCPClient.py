#!/usr/bin/env python
# -*- coding:utf8 -*-
import socket
import sys

HOST, PORT = "192.168.3.232", 8789
data = "<CloseAllWin,NPDS>"
#data = "<OpenSchema,NPDS,测试预案>"
print(data.encode("gb2312"))

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data.encode("gb2312"))
    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()
	
print("Sent:     {}".format(data))
print("Received: {}".format(received))