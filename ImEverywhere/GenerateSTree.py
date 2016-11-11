#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import jieba
# jieba 加载自定义词典
jieba.load_userdict("data/jieba/userdict.txt")
import jieba.analyse
# pynlpir
import pynlpir
from py2neo import Graph, Node, Relationship
from SemanticTree import SemanticTree
# TODO 分句
# from pyltp import SentenceSplitter


def GenerateSTree(NodeClass = "QA", Q = "Q", A = "A", words = None, tags = None, content = None, username = "Human"):
    """
    在图形数据库neo4j里建立QA语义关系图
    Q为question原句，A为answer原句，content为语义依存树，tags为Q关键词。
    usrname属性为当前用户名。可以为"Human"或者已经注册的用户名。
    sTreeRoot为语义树根节点，其它节点为"Semantic"类型，节点间关系用语义依存表示。
    	
    """
    graph = Graph("http://localhost:7474/db/data/", password = "gqy")
    sTreeNode = []
    isCreated = []
    sTreeRoot = Node(NodeClass, name = username, words = words, tags = tags, Q = Q, A = A)
    for word in content:
        node = Node("STree", name = (str(word["id"]) + "_" + word["cont"]), word = word["cont"], word_id = word["id"], pos = word["pos"], semparent = word["semparent"], semrelate = word["semrelate"])
        sTreeNode.append(node)
        isCreated.append(False)
    for index in range(len(sTreeNode)):
        semparent = content[index]["semparent"]
        if semparent == -1:
            node_semparent = Relationship(sTreeRoot, content[index]["semrelate"], sTreeNode[index])
        else:
            node_semparent = Relationship(sTreeNode[semparent], content[index]["semrelate"], sTreeNode[index])
        # 如果父节点不存在，先创建父节点
        if isCreated[semparent] == False:
            graph.create(sTreeNode[semparent])
        # 如果当前节点没有创建，那么创建
        if isCreated[index] == False:
            graph.create(sTreeNode[index])
        isCreated[index] = True
        graph.create(node_semparent)

if __name__ == '__main__':
    # pynlpir.open()
    f = open("data/topic/bank/semantic/xiaomin.txt", encoding="UTF-8")
    # 默认问题为单句	
    line = f.readline()
    while line:
        Q = line.rstrip()
        A = f.readline().rstrip()			
        print("Q: " + Q + "\nA: " + A)
		
        words = []
        tags = []
        # 1.分词，关键词提取。可用jieba或者nlpir。
        words = list(jieba.cut(Q))
        tags = jieba.analyse.extract_tags(Q, topK=10)
        # segments = pynlpir.segment(Q)
        # for segment in segments:
            # words.append(segment[0])	
        # tags = pynlpir.get_key_words(Q, weighted = False)

        # 2.语义依存树
        content = SemanticTree(Q)
        # 3.将每个句子的语义分析结果加入neo4j数据库
        for result in content:
            GenerateSTree(NodeClass="QA", Q=Q, A=A, words=words, tags=tags, content=result, username="Human")
        line = f.readline()
    f.close()
    # pynlpir.close()