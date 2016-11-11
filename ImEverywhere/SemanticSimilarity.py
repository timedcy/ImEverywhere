#/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import jieba
import numpy as np
from py2neo import Graph, Node, Relationship
# jieba.set_dictionary('data/jieba_dict/dict.txt.big')
	
def SynonymTag(words):
    """
    标注词向量的同义词词性向量
    如果词表中没有则暂标注为"NEW"
    
    """
    graph = Graph("http://localhost:7474/db/data/", password = "102422")
    semantic_vector = []
    for word in words:
        word_node = list(graph.find_one("synonym", "word", word))
        if word_node:
            word_tag = word_node[0]["tag"]
            semantic_vector.append(word_tag)
        else:
            semantic_vector.append("NEW")
    # print(semantic_vector)
    return semantic_vector

def SumCosine(matrix, threshold):
    """
    计算语义Jaccard中分子，即分词相似性矩阵的Cosine和
    
    """
    total = 0
    m = 0
    row = matrix.shape[0]
    col = matrix.shape[1]
    zero_row = np.zeros([1,col])
    zero_col = np.zeros([row,1])
    max = matrix.max()
    while max > threshold:
        total += max
        m += 1
        re = np.where(matrix == max)
        i = re[0][0]
        j = re[1][0]		
        matrix[i,:] = zero_row
        matrix[:,j] = zero_col
        max = matrix.max()
    return dict(total = total, m = m)
	
def SemanticJaccard(sv_sentence1, sv_sentence2):
    """
    语义Jaccard
    
    """
    sv_matrix = []
    sv_rows = []
	# 每两个词的相似度打分为[0,1]，阈值设定为0.5，若有任何一个为"NEW"则打分0.3
	# 标签字母前n位相同得分——7位：1，5位：0.95，4位：0.85，3位：0.75，2位：0.65，1位：0.55，0位：0.1
    for tag1 in sv_sentence1:
        for tag2 in sv_sentence2:
            if tag1 == "NEW" or tag2 == "NEW":
                score = 0.2
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
    matrix = np.mat(sv_matrix)
    # print(matrix)
	
    a = SumCosine(matrix, 0.7)
    b = SumCosine(matrix, 0)
    total = a["total"]
    total_dif = b["total"]
    m = b["m"]
    similarity = total/(total + m*(1-total_dif))
	
    return similarity

# TODO 语义编辑距离
def SemanticEditDistance(sv_sentence1, sv_sentence2):
    """
    语义编辑距离
    
    """    
    similarity = 1
    # print(str(similarity))
	
    return similarity

	
def Similarity(sv_sentence1, sv_sentence2, pattern = "jaccard"):
    """
    同义词词性向量相似度计算
    
    """ 
    similarity_jaccard = SemanticJaccard(sv_sentence1, sv_sentence2)
    similarity_edit = SemanticEditDistance(sv_sentence1, sv_sentence2)
	
    return similarity_jaccard if pattern == "jaccard" else similarity_edit

			
def SemanticSimilarity(words_sentence1, words_sentence2):
    """
    句子语义相似度计算
    
    """ 	
    sv_sentence1 = SynonymTag(words_sentence1)
    sv_sentence2 = SynonymTag(words_sentence2)    
    similarity = Similarity(sv_sentence1, sv_sentence2)	
    return similarity

if __name__ == "__main__":	
    print("语义相似度测试......") 
    filename = "log/SemanticSimilarity_" + time.strftime("%Y-%m-%d-%H-%M",time.localtime(time.time())) + ".md"
    f = open(filename, "w")
    f.write("标签：测试文档\n#语义相似度测试：\n>Enter the SemanticSimilarity mode...\n")

    while True:
        try:
            sentence1 = input("\nsentence1\n>>")
            sentence2 = input("sentence2\n>>")
            words_sentence1 = list(jieba.cut(sentence1))
            words_sentence2 = list(jieba.cut(sentence2))
            similarity = SemanticSimilarity(words_sentence1, words_sentence2)
            print("similarity: " + str(similarity))
            
            f.write("`>>" + sentence1 + "`\n")
            f.write("`>>" + sentence2 + "`\n")
            f.write("`" + "similarity: " + str(similarity) + "`\n")
        except KeyboardInterrupt:
            f.close()