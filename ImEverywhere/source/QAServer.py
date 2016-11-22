#!/usr/bin/env python3
# -*- coding:utf8 -*-
"""
Create TCPServer with socketserver.
The socketserver module simplifies the task of writing network servers.
"""
import chardet
import json
import simplejson
import socketserver
from QA import UnderstandContext

def recursive_json_loads(data):
    if isinstance(data, list):
        return [recursive_json_loads(i) for i in data]
    elif isinstance(data, tuple):
        return tuple([recursive_json_loads(i) for i in data])
    elif isinstance(data, dict):
        return Storage({recursive_json_loads(k): recursive_json_loads(data[k]) for k in data.keys()})
    else:
        try:
            obj = simplejson.loads(data)
            if obj == data:
                return data
        except:
            return data
        return recursive_json_loads(obj)


class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.
        >>> o = storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'
		

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        self.user = "user1"
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
            jdata = json.loads(self.data)
            question = jdata["ask_content"]
            #jdata = recursive_json_loads(self.data)
            #question = jdata.ask_content
            print("Q: " + question)
			
            # step 2.QA with NLP
            answer = UnderstandContext(question=question, username=self.user)
            print("A: " + answer)
			
			# step 3.str to json and send back the janswer
            janswer = json.dumps({"cmd":3,"content":answer,"emotion":2})
            self.request.sendall(janswer.encode(encoding))


if __name__ == "__main__":
    HOST, PORT = "192.168.4.72", 9999

    # Create the server, binding to localhost on port 9999
    qa = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    qa.serve_forever()