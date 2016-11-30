#!/usr/bin/env python
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
""" 
语料文本文件分词
"""
import codecs
import os
from string import punctuation
import jieba
jieba.set_dictionary("dict.txt.big")
jieba.load_userdict("userdict.txt")
import jieba.analyse


def read_file_cut():
	# 'mypunctuation' is the combination of Chinese and English punctuation.
    punctuation_zh = " 、，。°？！：；“”’‘～…【】（）《》｛｝×―－·→℃"
    punctuation_all = list(punctuation) + list(punctuation_zh)

    source_filename = "corpus.txt"
    result_filename = "result.txt"
    if os.path.exists(result_filename):
        os.remove(result_filename)
    with codecs.open(result_filename, 'w', "UTF-8") as result:
        with codecs.open(source_filename, 'r', "UTF-8") as source:    
            for line in source:
                if line != "":
                    line = line.rstrip('\n')
                    segments = jieba.cut(line, cut_all=False)
                    seglist = [segment for segment in segments if segment not in punctuation_all]
                    output = ' '.join(seglist)
                    result.write(output + ' ')
            result.write('\r\n')
    print("Successfully read files and segmentation!")
			
if __name__ == '__main__':
    read_file_cut()
