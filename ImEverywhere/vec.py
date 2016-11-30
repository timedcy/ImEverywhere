#/usr/bin/env python3
# -*- coding: utf-8 -*-
# 测试完善中

import numpy
import jieba
jieba.set_dictionary("./data/jieba/dict.txt.big")
jieba.load_userdict("./data/jieba/userdict.txt")
import jieba.posseg
import jieba.analyse
from gensim.models.word2vec import Word2Vec
model = Word2Vec.load_word2vec_format("./data/vectors.bin", binary=True)
from mytools import time_me, get_current_time

def word_similarity(w1, w2):
    return model.similarity(w1, w2)
	
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
        re = numpy.where(matrix==max)
        i = re[0][0]
        j = re[1][0]		
        matrix[i,:] = zero_row
        matrix[:,j] = zero_col
        max = matrix.max()
    m = (row - count) if row > col else (col - count)
    return dict(total=total, m=m, total_dif=max)
	
@time_me()	
def vec_jaccard(sentence1, sentence2, pattern = 'w'):
    """
    向量语义Jaccard, 返回向量语义相似度打分
    """
    sv_matrix = []
    sv_rows = []
    if pattern == 'w':
        sv1 = list(jieba.cut(sentence1))
        sv2 = list(jieba.cut(sentence2))
    elif pattern == 't':
        sv1 = jieba.analyse.extract_tags(sentence1, topK=10)
        sv2 = jieba.analyse.extract_tags(sentence2, topK=10)
    print(sv1, sv2)
	# 根据训练好的vectors.bin建模来计算相似度。阈值设定为0.6，每两个词的相似度打分为[0,1]
    for w1 in sv1:
        for w2 in sv2:
            score = word_similarity(w1, w2)
            sv_rows.append(score)
        sv_matrix.append(sv_rows)
        sv_rows = []	
    matrix = numpy.mat(sv_matrix)	
    result = sum_cosine(matrix, 0.6)
    total = result["total"]
    total_dif = result["total_dif"]
    m = result["m"]
    similarity = total/(total + m*(1-total_dif))
	
    return similarity
	
if __name__ == '__main__':
    print("向量语义相似度测试......") 
    filename = "log/VecSimilarity_" + get_current_time() + ".md"
    f = open(filename, "w")
    f.write("标签：测试文档\n#向量语义相似度测试：\n>Enter the VecSimilarity mode...\n")

    while True:
        try:
            sentence1 = input("\nsentence1\n>>")
            sentence2 = input("sentence2\n>>")
            similarity = vec_jaccard(sentence1, sentence2, 'w')
            print("similarity: " + str(similarity))
            similarity = vec_jaccard(sentence1, sentence2, 't')
            print("similarity: " + str(similarity))
            
            f.write("`>>" + sentence1 + "`\n")
            f.write("`>>" + sentence2 + "`\n")
            f.write("`" + "similarity: " + str(similarity) + "`\n")
        except KeyboardInterrupt:
            f.close() 