#!/usr/bin/env python
# -*- coding:utf8 -*-
import socket
from time import ctime

HOST = "192.168.4.72"
PORT = 9999
BUFSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(5)

while True:
    print("waiting for connection...")
    connection, addr = sock.accept()
    print("...connected from:", addr)

    while True:
	    # ASR data (text or hex data)
        data = connection.recv(BUFSIZE)
        if not data:
            break
		# NLP with text of question
        print(data)
		# Answer data (text or hex data)
        connection.send("[%s] %s" %(ctime(),data))
sock.close()