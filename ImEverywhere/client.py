# -*- coding: utf-8 -*-
import json
import socket
#import chardet


def json_pack(info):
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
		
def match(question = "question", username = "Human"):
    # local_ip = socket.gethostbyname(socket.gethostname())
    # print(local_ip)
    HOST, PORT = "localhost", 9999
    bufsize = 1024
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    answer = "answer"
    print("question: " + question)
    print("username: " + username)
    try:
        # Connect to server
        sock.connect((HOST, PORT))
        # step 1.pack input
        json_data = json_pack(question)
        # step 2.send and receive data
        sock.sendall(json_data.encode("UTF-8"))
        received = sock.recv(bufsize)
        #encoding = chardet.detect(received)["encoding"]
        #print(encoding)
        #received = received.decode(encoding)
        received = received.decode("UTF-8")
        json_received = json.loads(received)
        # step 3.extract answer
        answer = json_received["content"]
        print("A: " + answer)
    finally:
        sock.close()
    return answer
	
if __name__ == '__main__':
    question = u"什么是云账户"
    match(question=question)
