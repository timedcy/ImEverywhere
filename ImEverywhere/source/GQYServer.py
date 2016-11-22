#!/usr/bin/env python3
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""
Create GQY TCPServer with socketserver.
The socketserver module simplifies the task of writing network servers.
"""
import json
import chardet
import socketserver
from QA import UnderstandContext


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        self.user = "root"
        while True:
			# self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024)
            if not self.data:
                break
            print("{} wrote:".format(self.client_address[0]))
            # detect encoding of self.data
            encoding = chardet.detect(self.data)["encoding"]
            print("encoding: " + encoding)
            # step 1.bytes to json obj and extract question
            self.data = self.data.decode(encoding)
            json_data = json.loads(self.data)
            print(json_data)
            if json_data.get("cmd"):
                if json_data["cmd"] == 8:
                    janswer = json.dumps({"cmd":8}) + "\r\n"
                    self.request.sendall(janswer.encode(encoding))
            if json_data.get("action"):
                if json_data["action"] == 1:
                    janswer = json.dumps({"cmd":8}) + "\r\n"
                    self.request.sendall(janswer.encode(encoding))
                if json_data["action"] == 2:
                    question = json_data["ask_content"]
                    print("Q: " + question)
				    # step 2.QA with NLP
                    answer = UnderstandContext(question=question, username=self.user)
                    print("A: " + answer)
				    # step 3.str to json and send back the janswer
                    janswer = json.dumps({"cmd":3, "content":answer, "emotion":2}) + "\r\n"
                    self.request.sendall(janswer.encode(encoding))

def start_server(host, port):
    """
    Start server with host and port.

    The QA mode of connection.
    """
    # Create the server, binding to localhost on port 9999
    sock = socketserver.TCPServer((host, port), MyTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    sock.serve_forever()

if __name__ == "__main__":
    HOST, PORT = "192.168.4.72", 9999
    start_server(HOST, PORT)
	