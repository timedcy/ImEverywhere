#!/usr/bin/env python3
# -*- coding:utf8 -*-

import json
from urllib import request

def SemanticTree(question):
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
    # print(content_str)
    content_json = json.loads(content_str)

    return content_json[0]

	
if __name__ == '__main__':
    # 单句 simple sentence
    question = "我想买一张明天上海到北京的机票。"
    # 复句 compound sentences
    # question = "我想买一张明天上海到北京的机票。请问您能帮我订票吗？"
    content = SemanticTree(question)
    for sentence in content: 
        print(sentence)
        print("\n")
    print(str(len(content)) + (" sentences\n" if len(content) > 1 else " sentence only\n"))
    # 文本 text
    # fh = open("data/train.txt", encoding = "UTF-8")
    # for line in fh:
        # print(line)
        # content = SemanticTree(line)
        # print(content)
        # print(str(len(content)) + (" sentences\n" if len(content) > 1 else " sentence only\n"))
