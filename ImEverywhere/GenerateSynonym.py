#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
jieba.load_userdict("data/jieba/userdict.txt")
import jieba.posseg as pseg
from py2neo import Graph, Node, Relationship

def Handle(line):
    content = line.split()
    return content

def GenerateSynonym(content):
    """
    在图形数据库neo4j里建立Synonym同义词关系图
    hot为同义词热度
	
    """
    graph = Graph("http://localhost:7474/db/data/", password="gqy")
    classification = content[0]
    words = content[1:]
    synonym_root = Node("SynonymTag", name=classification, words=words, hot=0)
    graph.create(synonym_root)
    for word in words:
        for w in pseg.cut(word):
            flag = w.flag
        synonym_node = Node("synonym", name=word, tag=classification, pos=flag, hot=0)
        root_contain_node = Relationship(synonym_root, "contain", synonym_node)
        graph.create(root_contain_node)

if __name__ == '__main__':
    with open("data/synonym.txt", encoding="UTF-8") as file:
        for line in file:
            print(line)
            content = Handle(line)
            GenerateSynonym(content)