# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from sTreeAPI import sTreeAPI
from HandlingQuestion import analyseJieba, analyseLtp, analyseNlpir

def testsTreeAPI(question):
    print(sys._getframe().f_code.co_name)
    content = sTreeAPI(question)
    print(content)
    print(str(len(content)) + " sentences" if isinstance(content[0], list) else "1 sentence only")

def testJieba(question):
    print(sys._getframe().f_code.co_name)
    database_request = analyseJieba(question)
    print(database_request)
	
def testLtp(question):
    print(sys._getframe().f_code.co_name)
    database_request = analyseLtp(question)
    print(database_request)
	
def testNlpir(question):
    print(sys._getframe().f_code.co_name)
    database_request = analyseNlpir(question)
    print(database_request)

if __name__ == "__main__":
    question = "我想买一张明天上海到北京的机票。"
    testsTreeAPI(question)
    testJieba(question)
    testNlpir(question)
    testLtp(question)