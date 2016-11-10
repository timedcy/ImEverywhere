#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
Create TCPServer with SocketServer.
The SocketServer module simplifies the task of writing network servers.
"""
import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        while True:
			# self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024)
            if not self.data:
                break
            print("{} wrote:".format(self.client_address[0]))
            self.data = self.data.strip()
            print(self.data)
            # just send back the same data, but upper-cased
            self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "192.168.4.72", 9999

    # Create the server, binding to localhost on port 9999
    qa = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    qa.serve_forever()
	