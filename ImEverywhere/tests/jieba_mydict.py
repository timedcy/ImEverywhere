# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import jieba
import jieba.posseg
import jieba.analyse

jieba.load_userdict("../data/jieba_dict/userdic.dic")

content = "黄河入海流"
result = jieba.posseg.cut(content)

for w in result:
    print(w.word, "/", w.flag, ", ", end=' ')