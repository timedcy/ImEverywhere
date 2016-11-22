#/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy
import json
import jieba
jieba.set_dictionary("data/jieba/synonymdict.txt")
#jieba.load_userdict("data/jieba/userdict.txt")
import jieba.posseg
import jieba.analyse
from urllib import request
from mytools import time_me, get_current_time
from py2neo import Graph, Node, Relationship
graph = Graph("http://localhost:7474/db/data/", password = "gqy")

def semantic_tree(question):
    """
    1.API 会自动断句并将各句分析结果一并返回，每个句子切词后首个词"id": 0
    2.若为单句返回原单句分析列表，若为复句返回断句后的各单句分析列表总和
    3.参数设定参考'http://www.ltp-cloud.com/document/#api_rest_param'，其中"pattern" 用以指定分析模式
    pattern：ws(分词)，pos(词性标注)，ner(命名实体识别)，dp(依存句法分析)，sdp(语义依存分析)，srl(语义角色标注)，all(全部任务)
    4.返回值'content_json[0]'是一个包含每个句子分析结果的列表。   	
    """	
    url_get_base = "http://api.ltp-cloud.com/analysis/?"
    api_key = "97K7s6t8OSEwXtLZDN3FtyBi2FzRsAxPxv8GRNfz"
    text = request.quote(question)
    format = "json"
    pattern = "all"
    
    result = request.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,text,format,pattern))
    content_bytes = result.read()
    content_str = content_bytes.decode("UTF-8")
    content_json = json.loads(content_str)
	
    strees = content_json[0]
    print(str(len(strees)) + (" sentences\n" if len(content) > 1 else " sentence only\n"))
    return strees

def generate_qa(NodeClass = "QA", Q = "Q", A = "A", words = None, tags = None, username = "Human"):
    node = Node(NodeClass, Q=Q, A=A, words=words, tags=tags, username=username)
    graph.create(node)

def generate_tree(NodeClass = "STree", Q = "Q", A = "A", content = None, username = "Human"):
    """
    在图形数据库neo4j里建立QA语义依存树
    Q为question原句，A为answer原句，content为语义依存树。
    usrname属性为当前用户名。可以为"Human"或者已经注册的用户名。
    语义树根节点类型为'STree'，其它节点为'SWord'类型，节点间关系用语义依存表示。
    	
    """
    sTreeNode = []
    isCreated = []
    words = [word["cont"] for word in content]
    sTreeRoot = Node(NodeClass, name = username, Q = Q, A = A)
    for word in content:
        node = Node("SWord", name = (str(word["id"]) + "_" + word["cont"]), word = word["cont"], word_id = word["id"], pos = word["pos"], semparent = word["semparent"], semrelate = word["semrelate"])
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
		
@time_me()
def jaccard(sv1, sv2):
    """
    基础Jaccard匹配相似度
    """
    count_intersection = list(set(sv1).intersection(set(sv2)))
    count_union = list(set(sv1).union(set(sv2)))
    similarity = len(count_intersection)/len(count_union)
    return similarity
		
def synonym_cut(sentence, pattern = "wf"):
    """
    自定义句子切分为同义词标签
    如果同义词词典中没有则标注为切词工具默认的词性    
    """
    sv = []
    if pattern == "w":
        sv = list(jieba.cut(sentence))
    elif pattern == "t":		
        sv = jieba.analyse.extract_tags(sentence, topK=10)		
    elif pattern == "wf":
        result = jieba.posseg.cut(sentence)
        sv = [w.flag for w in result]
    elif pattern == "tf":
        result = jieba.posseg.cut(sentence)
        tags = jieba.analyse.extract_tags(sentence, topK=10)
        for w in result:
            if w.word in tags:
                sv.append(w.flag)			
    return sv
	
@time_me()	
def synonym_tag(words):
    """
    标注词向量的同义词分类标签
    如果词表中没有则标注为原词    
    """
    sv = []
    for word in words:
        word_node = graph.find_one("Synonym", "name", word)
        if word_node:
            word_tag = word_node["tag"]
            sv.append(word_tag)
        else:
            sv.append(word)
    return sv

def sum_cosine(matrix, threshold):
    """
    1.计算语义Jaccard中分子total，即分词相似性矩阵的Cosine和
    2.计算m: 两个集合中没有达到语义匹配标准（由阈值threshold控制）的总片段个数或者两者中取最大值
    """
    total = 0
    count = 0
    row = matrix.shape[0]
    col = matrix.shape[1]
    zero_row = numpy.zeros([1,col])
    zero_col = numpy.zeros([row,1])
    max = matrix.max()
    while max > threshold:
        total += max
        count += 1
        re = numpy.where(matrix == max)
        i = re[0][0]
        j = re[1][0]		
        matrix[i,:] = zero_row
        matrix[:,j] = zero_col
        max = matrix.max()
    m = (row - count) if row > col else (col - count)
    return dict(total=total, m=m, total_dif=max)

#@time_me()	
# TODO: Add word2vec
def semantic_jaccard(sv1, sv2):
    """
    语义Jaccard, 返回向量语义相似度打分
    """
    sv_matrix = []
    sv_rows = []
	# 阈值设定为0.8，每两个词的相似度打分为[0,1]，若无标签则计算原词相似度得分
	# 标签字母前n位相同得分——7位：1，5位：0.95，4位：0.85，3位：0.75，2位：0.65，1位：0.55，0位：0.1
    for tag1 in sv1:
        for tag2 in sv2:
            if tag1 == tag2:
                score = 1
            elif tag1[:7] == tag2[:7]:
                score = 1
            elif tag1[:5] == tag2[:5]:
                score = 0.95
            elif tag1[:4] == tag2[:4]:
                score = 0.85
            elif tag1[:3] == tag2[:3]:
                score = 0.75
            elif tag1[:2] == tag2[:2]:
                score = 0.65
            elif tag1[:1] == tag2[:1]:
                score = 0.55
            else:
                score = 0.1
            sv_rows.append(score)
        sv_matrix.append(sv_rows)
        sv_rows = []	
    matrix = numpy.mat(sv_matrix)	
    result = sum_cosine(matrix, 0.8)
    total = result["total"]
    total_dif = result["total_dif"]
    m = result["m"]
    similarity = total/(total + m*(1-total_dif))
	
    return similarity

# TODO 语义编辑距离
def semantic_edit_distance(sv1, sv2):
    """
    语义编辑距离
    
    """    
    similarity = 1
    # print(str(similarity))
	
    return similarity

#@time_me()			
def semantic_similarity(sv1, sv2, pattern = "sj"):
    """
    句子向量语义相似度计算
    
    """ 
    if pattern == "j":	
        similarity = jaccard(sv1, sv2)
        return similarity		
    if pattern == "sj":
        similarity = semantic_jaccard(sv1, sv2)
    elif pattern == "e":	
        similarity = semantic_edit_distance(sv1, sv2)
    return similarity

def synonym_sentence(words):
    """
    词向量替换为随机同义词向量，词分类节点为"SynonymTag"，词节点为"Synonym"
    
    """
    graph = Graph("http://localhost:7474/db/data/", password = "gqy")
    sv = []
    for word in words:
        word_node = graph.find_one("Synonym", "word", word)
        if word_node:
            tag_node = graph.find_one("SynonymTag", "name", word_node["tag"])
            tag_words = tag_node["words"]
            synonym_random = tag_words[random.randint(0, len(tag_words)-1)]
            sv.append(synonym_random)   
    return sv	

if __name__ == "__main__":	
    print("语义相似度测试......") 
    filename = "log/SemanticSimilarity_" + get_current_time() + ".md"
    f = open(filename, "w")
    f.write("标签：测试文档\n#语义相似度测试：\n>Enter the SemanticSimilarity mode...\n")

    while True:
        try:
            sentence1 = input("\nsentence1\n>>")
            sentence2 = input("sentence2\n>>")
            w1 = synonym_cut(sentence1, 't')
            w2 = synonym_cut(sentence2, 't')
            sv1 = synonym_cut(sentence1, 'wf')
            sv2 = synonym_cut(sentence2, 'wf')
            print(w1, w2)
            similarity = semantic_similarity(w1, w2)
            print("similarity: " + str(similarity))
            print(sv1, sv2)
            similarity = semantic_similarity(sv1, sv2)
            print("similarity: " + str(similarity))
            
            f.write("`>>" + sentence1 + "`\n")
            f.write("`>>" + sentence2 + "`\n")
            f.write("`" + "similarity: " + str(similarity) + "`\n")
        except KeyboardInterrupt:
            f.close()