#!/usr/bin/env python3
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""
Question and answer with Natural Language Processing and Graph Database.
The 'pynlpir' and 'jieba' are Chinese word segmentation tools.
The 'py2neo' is a python package of neo4j, the most useful graph database.
"""
import sys
import os
import time
import pynlpir
import jieba
# jieba 自定义词典
jieba.load_userdict("data/jieba/userdict.txt")
import jieba.analyse
from py2neo import Graph, Node, Relationship
from SemanticTree import SemanticTree
from GenerateSTree import GenerateSTree
import API
from SynonymousSentence import SynonymousSentence
from SemanticSimilarity import SemanticSimilarity


def GetNowTime():
    return time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
	
def AddToMemory(question="question", words=None, content=None, tags=None, username="User"):
    """
    将用户当前语句的语义分析结果加入信息记忆	
    """
	# 添加到记忆链，每一类型的节点都需要重构
    qaID = username + "_" + GetNowTime()
    for pos in range(len(content)):
        GenerateSTree(NodeClass="Memory", Q=question, words=words, content=content[pos], tags=tags, username=username)	
	
def ContextClassify(tags, username):
    """
    根据上下文判断关键词的话题    
    """
    graph = Graph("http://localhost:7474/db/data/", password="gqy")
    parameters = tags
    current_topic = ""
    topic_node = None
    isEnter = False
    root = graph.find_one("User", "name", username)
    if root["memory_from"]: 
        current_topic = root["memory_from"][-1]
        topic_node = graph.find_one("topic", "name", current_topic)
    print("Current topic: " + current_topic)
    previous_tags = root["memory_tags"][-1].split("|") if root["memory_tags"] else []
    print("Memory tags:")
    print(previous_tags)

    # 1.如果发现跳出了当前话题，那么在记忆中选取除当前话题外的最近话题，判断其是否符合当前语境
	# 2.若最近话题符合，那么继续最近话题聊天；若不符合，那么选取次近话题进行判断，依此类推
	# 3.若记忆中所有话题都不符合语境，那么表示开启了新的话题，重新遍历话题来判断
    for topic in root["items"]:
	    # TODO 对topic根据优先级排序存储，每次先从优先级高的话题开始匹配，避免话题重复
        node = graph.find_one("topic", "name", topic)
        if list(set(node["items"]).intersection(set(tags))):
            isEnter = True
            root["hot"] += 1
            node["hot"] += 1
            if not current_topic:
                node["memory_from"].append(current_topic)
            relationship = graph.match(start_node=topic_node, rel_type="Then", end_node=node)
            if list(relationship):
			    # parameters循环过滤
                parameters = list(set(parameters).difference(set(topic_node["items"])))
				# 上下文记忆参数传递，循环筛选与当前语义不重复的部分，整合到当前参数
                previous_tags = list(set(previous_tags).difference(set(node["items"])))
            else:
                # 若有多个话题并存则选取优先级最高的一个作为主话题 
                if current_topic != topic:
                    current_topic = topic
                    print("Topic changed to " + current_topic)
                    root["memory_to"].append(current_topic)
                    root["memory_from"].append(current_topic)
                    topic_node = graph.find_one("topic", "name", current_topic)
                parameters = list(set(parameters).difference(set(node["items"])))
                # print(parameters)
            node["memory_to"].append(current_topic)
            graph.push(node)

	# 添加当前混合参数到记忆中，这样就实现了语义的上下文传递
    if isEnter:
        parameters += previous_tags
        root["memory_tags"].append("|".join(parameters))
        graph.push(root)
    print("Current tags:")
    print(parameters)
    result = dict(topic=current_topic, parameters=parameters)
    return result
	
def UnderstandContext(question="question", username="root", tool="jieba"):
    """
    上下文语境理解
    """
    words = []
    answer = None
    classify = None
    if tool == "pynlpir":
        pynlpir.open()
        segments = pynlpir.segment(question)
        for segment in segments:
            words.append(segment[0])
        tags = pynlpir.get_key_words(question, weighted=False)
        pynlpir.close()
    elif tool == "jieba":
        words = list(jieba.cut(question))
        tags = jieba.analyse.extract_tags(question, topK=10)
        print(tags)
    # content = SemanticTree(question)
    # 将用户当前语句的语义分析结果加入信息记忆 TO UPDATE 'Classify' in GenerateSTree
    # AddToMemory(question=question, words=words, content=content, tags=tags, username=username)
    # 结合上下文进行话题标注，语义判断，以及参数抽取
    classify = ContextClassify(tags, username=username)
    # 查询匹配答案
    if classify["parameters"]:
        answer = API.topic_query(topic=classify["topic"], parameters=classify["parameters"])
    else:
        answer = "关于这个问题我正在学习中，哈哈"
    return answer

	
def ExtractSynonym(words, subgraph):
    """
    从图形数据库返回的搜索结果列表选取相似度最高的同义句
    """
    similarity = []
    for node in subgraph:
        ss = SemanticSimilarity(words, node["words"])
        similarity.append(ss)
    index = similarity.index(max(similarity))
    return subgraph[index]["A"]

# TODO
def ExtractSTree(content, subgraph):
    """
    从图形数据库返回的搜索结果列表选取相似度最高的语义树	
    """
    similarity = []
    for node in subgraph:
        ss = TreeSimilarity(content, node["content"])
        similarity.append(ss)
    index = similarity.index(max(similarity))
    return subgraph[index]["A"]
	
# TODO
def CreateSentence():
    """
    答案语句的自动生成	
    """
    return "This is created by AI."

def SearchDatabase(question="question", username="Human"):
    """
    username属性可为Human或Robot,也可是某个已注册用户的名字。
    qaID是当前用户输入在整个对话上下文信息中的ID。
    subgraph = graph.find("Human", "keywords", tags, 10)
    默认返回前10项,此处为Human类型的Node
    """
    graph = Graph("http://localhost:7474/db/data/", password="gqy")
    words = []
    pynlpir.open()
	# TODO: 处理复句中每个分句的关键词
	# words = list(jieba.cut(question))
    # tags = jieba.analyse.extract_tags(question, topK=5)
    segments = pynlpir.segment(question)
    for segment in segments:
        words.append(segment[0])	
    tags = pynlpir.get_key_words(question, weighted=False)
    pynlpir.close()
    content = SemanticTree(question)
	# 将用户当前语句的语义分析结果加入信息记忆   
    AddToMemory(question=question, words=words, content=content, tags=tags, username=username)
    # 问题关键词匹配
    subgraph = graph.find_one("Service", "keywords", tags)
    print(subgraph)
    if subgraph:
	    # 直接选取
        answer = subgraph.A
        # 问题语义匹配，抽取同义句
        # answer = ExtractSynonym(words, subgraph)
        # 语义依存树相似度匹配，抽取语义树 TODO
        # answer = ExtractSTree(content, subgraph)
    else:
        # 添加随机回答 TODO
        answer = "关于这个问题我正在学习中，哈哈"		
    return answer.rstrip()
