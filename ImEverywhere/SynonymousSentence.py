#/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import random
import jieba
import pynlpir
from py2neo import Graph, Node, Relationship

def SynonymReplace(words):
    """
    词向量替换为同义词向量，同义词表存储在neo4j数据库中，词性根节点为"SynonymRoot"，词节点为"synonym"
    
    """
    graph = Graph("http://localhost:7474/db/data/", password = "gqy")
    sv = []
    for word in words:
        word_node = list(graph.find("synonym", "word", word, 1))
        if word_node:
            synonym_node = list(graph.find("Synonyms", "name", word_node[0]["tag"], 1))
            synonym_words = synonym_node[0]["words"]
            synonym_random = synonym_words[random.randint(0, len(synonym_words)-1)]
            sv.append(synonym_random)   
    return sv
	
def SynonymousSentence(question, tool="jieba"):
    """
    生成同义句。分词工具可选择jieba或者nlpir，支持其它或者自定义分词工具扩展。
    	
    """	
    words = []
    if tool == "jieba":	
        words = list(jieba.cut(question))
    elif tool == "nlpir":
        pynlpir.open()
        segments = pynlpir.segment(question)
        for segment in segments:
            words.append(segment[0])
        pynlpir.close()
    print(tool + " cut: " + "/".join(words))
  
    sv = SynonymReplace(words)  
    print(tool + " generate: " + "/".join(sv))
    answer = "".join(sv)
    
    return answer

if __name__ == "__main__":
	print("同义句生成测试......") 
	filename = "log/SynonymousSentence_" + time.strftime("%Y-%m-%d-%H-%M",time.localtime(time.time())) + ".md"
	f = open(filename, "w")
	f.write("标签：测试文档\n#同义句生成测试：\n>Enter the SynonymousSentence mode...\n")

	while True:
		try:
			question = input("\n>>")
			answer_jieba = SynonymousSentence(question, tool = "jieba")
			answer_nlpir = SynonymousSentence(question, tool = "nlpir")
			print("answer_jieba: " + answer_jieba)
			print("answer_nlpir: " + answer_nlpir)

			f.write("`>>" + question + "`\n")
			f.write("`answer_jieba: " + answer_jieba + "`\n")
			f.write("`answer_nlpir: " + answer_nlpir + "`\n")
		except KeyboardInterrupt:
			f.close()