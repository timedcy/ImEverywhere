#!/usr/bin/env python3
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""
Create GQY TCPClient with socket.
The send data need to be packed with json.
"""
import json
import socket
import chardet

def jsonpack(info):
    """
    Pack send data with json.

    The send data format must adapt to data transmission protocolIt of robot.
    """
    data = {"from":"android",
            "action":2,
            "sn":"A000000001",
            "key":"A000000001",
            "is_need_reply":1,
            "ask_content":info,
            "answer_iflytek":"黑色",
            "answer_tuling":"白色",
            "answer_content":"黑白色",
            "state":1}
    return json.dumps(data)

def connect_server(host, port, bufsize):
    """
    Connect server with host and port.

    The QA mode of connection.
    """
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to server
        sock.connect((host, port))
        while True:
            try:
                # pack input
                question = input("Q:>")
                json_data = jsonpack(question)
                # send and receive data
                sock.sendall(json_data.encode("UTF-8"))
                received = sock.recv(bufsize)
                encoding = chardet.detect(received)["encoding"]
                print(encoding)
                received = received.decode(encoding)
                json_received = json.loads(received)
                # extract answer
                answer = json_received["content"]
                print("A: " + answer)
            except KeyboardInterrupt:
                print("Exit QA")
    finally:
        sock.close()

if __name__ == "__main__":
    HOST, PORT = "192.168.4.72", 9999
    BUFSIZE = 1024
    connect_server(HOST, PORT, BUFSIZE)
	