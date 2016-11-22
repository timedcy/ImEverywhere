#!/usr/bin/env python3
# -*- coding:utf8 -*-
import chardet
import json
import socket
import sys

def jsonpack(info):
    data = {"from":"android",
            "action":2,
            "sn":"A000000001",
            "key":"A000000001",
            "is_need_reply":1,
            "ask_content":info,
            "answer_iflytek":"黑色",
            "answer_tuling":"白色",
            "answer_content":"黑白色",
            "state":1
            }
    jdata = json.dumps(data)
    return jdata
	
HOST, PORT = "192.168.4.72", 9999
# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect to server
    sock.connect((HOST, PORT))
    while True:
        try:
		    # pack input
            question = input("Q:>")
            jdata = jsonpack(question)
			# send and receive data
            sock.sendall(jdata.encode("UTF-8"))
            received = sock.recv(1024)
            encoding = chardet.detect(received)["encoding"]
            received = received.decode(encoding) 
            jreceived = json.loads(received)
            # extract answer
            answer = jreceived["content"]
            print("A: " + answer)
        except KeyboardInterrupt:
            print("Exit QA")    
finally:
    sock.close()