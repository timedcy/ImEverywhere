# -*- coding: utf-8 -*-

import sys
import pynlpir

pynlpir.open()

#s = '我想买一张明天上海到广州的机票'
s = '海上生明月，天涯共此时'
segments = pynlpir.segment(s)
for segment in segments:
    print(segment[0], '\t', segment[1])
	
key_words = pynlpir.get_key_words(s, weighted=True)
for key_word in key_words:
    print(key_word[0], '\t', key_word[1])
	
s1 = '我想去云南旅游，用什么交通工具好？'
segments = pynlpir.segment(s1, pos_names='all', pos_english=False)
for segment in segments:
    print(segment[0], '\t', segment[1])

key_words = pynlpir.get_key_words(s1, weighted=True)	
#key_words = pynlpir.get_key_words(s1, weighted=False)
for key_word in key_words:
    print(key_word[0], '\t', key_word[1])
	#print(key_word)

pynlpir.close()