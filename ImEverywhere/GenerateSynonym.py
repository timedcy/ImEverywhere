# -*- coding: utf-8 -*-
import jieba.posseg as pseg
from py2neo import Graph, Node, Relationship

def Handle(line):
    synonym = line.split()
    return synonym

def GenerateSynonym(synonym):
    """
    在图形数据库neo4j里建立Synonym同义词关系图
    hot为同义词热度
	
    """
    graph = Graph("http://localhost:7474/db/data/", password="gqy")
    classification = synonym[0]
    words = synonym[1:]
    SynonymRoot = Node("Synonyms", name=classification, words=words, hot=0)
    graph.create(SynonymRoot)
    for word in words:
        for w in pseg.cut(word):
            flag = w.flag
        node = Node("synonym", word=word, tag=classification, pos=flag, hot=0)
        node_SynonymRoot = Relationship(SynonymRoot, "contain", node)
        graph.create(node_SynonymRoot)

if __name__ == '__main__':
    with open("data/synonym.txt", encoding="UTF-8") as file:
        for line in file:
            print(line)
            synonym = Handle(line)
            GenerateSynonym(synonym)