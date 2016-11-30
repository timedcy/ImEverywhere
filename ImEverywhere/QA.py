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
# import pynlpir
from py2neo import Graph, Node, Relationship
graph = Graph("http://localhost:7474/db/data/", password="gqy")
import api
from semantic import semantic_similarity, synonym_cut, generate_tree
from mytools import time_me, get_current_time, random_item

# TODO	
def add_to_memory(Q="Q", words=None, tags=None, content=None, username="Human"):
    """
    将用户当前语句的语义分析结果加入信息记忆	
    """
	# 添加到记忆链，每一类型的节点都需要重构
    qaID = username + "_" + get_current_time()
    for semantic_tree in content:
        generate_tree(NodeClass="Memory", Q=Q, words=words, content=semantic_tree, tags=tags, username=username)	
	
def context_classify(tags, username):
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
	
def understand_context(question="question", username="root", tool="jieba"):
    """
    上下文语境理解
    """
    answer = None
    classify = None
    words = synonym_cut(question, 'w')
    tags = synonym_cut(question, 't')
    # content = SemanticTree(question)
    # 将用户当前语句的语义分析结果加入信息记忆 TO UPDATE 'Classify' in generate_tree
    # add_to_memory(Q=question, words=words, tags=tags, content=content, username=username)
    # 结合上下文进行话题标注，语义判断，以及参数抽取
    classify = context_classify(tags, username=username)
    # 查询匹配答案
    if classify["parameters"]:
        answer = API.topic_query(topic=classify["topic"], parameters=classify["parameters"])
    else:
        answer = "关于这个问题我正在学习中，哈哈"
    return answer

	
def extract_synonym(question, subgraph, pattern = "wf"):
    """
    从图形数据库返回的搜索结果列表选取相似度最高的语义Jaccard匹配同义句
    pattern可选'w'-分词, 't'-关键词, 'wf'-分词标签, 'tf-关键词标签'
    """
    similarity = []
    answer = "您好！请问有什么可以帮您的吗？"
    do_not_know = ["正在学习中", "小民正在学习哦", "不好意思请问您可以再说一次吗", "额，这个问题嘛。。。", "我得好好想一想呢", "请问您说什么", "。。。", "您问的问题好有深度呀"]
    command = {"time":["几点了", "现在几点了", "现在时间", "现在时间是多少"], "cmd":["打电话", "打电话给"]}
    if question in command["time"]:
        answer = get_current_time("现在是%Y年%m月%d日%H点%M分%S秒")
        return answer
    elif question in command["cmd"]:
        answer = "正在连接中，请稍候"
        return answer
    sv1 = synonym_cut(question, pattern)
    for node in subgraph:
        sv2 = synonym_cut(node["Q"], pattern)
        ss = semantic_similarity(sv1, sv2, pattern="sj")
        similarity.append(ss)
    max_similarity = max(similarity)
    print("Similarity Score: " + str(max_similarity))
    index = similarity.index(max_similarity)
    Q = subgraph[index]["Q"]
    A = subgraph[index]["A"]	
    print("Q: " + Q)
    if max_similarity > 0.2:
        if isinstance(A, list):
            answer = random_item(A)
    else:
	    # 随机回答
        answer = random_item(do_not_know)
    return answer

# TODO
def extract_tree(node, subgraph):
    """
    从图形数据库返回的搜索结果列表选取相似度最高的语义树	
    """
    similarity = []
    for node in subgraph:
	    # 语义树相似度计算
        ss = TreeSimilarity(node, node["content"])
        similarity.append(ss)
    index = similarity.index(max(similarity))
    return subgraph[index]["A"]
	
# TODO
def create_sentence():
    """
    答案语句的自动生成	
    """
    return "This is created by AI."

@time_me()
def search_database(question="question", username="Human"):
    """
    username属性为某个已注册用户的名字，默认为"Human"。
    搜索与问题相关的子图，选取语义相似度最高的QA备选项
    """
    subgraph = list(graph.find("QA", "username", username))
    if subgraph:
	    # 多模式匹配问句选取相似度最高的问句
        # answer = extract_synonym(words, subgraph, key="words")
        answer = extract_synonym(question, subgraph, pattern = "wf")
        # 语义依存树相似度匹配，抽取相似度最高语义树 TODO
        # answer = extract_tree(sv, subgraph)
    else:
        answer = "欢迎您注册哦"		
    return answer.rstrip()
