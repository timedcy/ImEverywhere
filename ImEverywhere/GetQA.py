#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2016.11.7
# @Function: Agile Software Development——Excel 
# @Author  : Rain

import os
import string
import xlrd
import xlwt
import jieba
jieba.load_userdict("data/jieba/userdict.txt")
import jieba.analyse
from SemanticTree import SemanticTree
from GenerateSTree import GenerateSTree

def get_data_excel(filepath):
    """Get excel source"""
    is_valid = False   
    try:
        # if it is xls
        if os.path.isfile(filepath):
            filename = os.path.basename(filepath)
            if filename.split('.')[1] == 'xls':
                is_valid = True
        data = None
        if is_valid:
            data = xlrd.open_workbook(filepath)
    except Exception as e:
        print('Error：%s' %e)
        return None
    return data


def handle_data_excel(filepath):
    """Processing data to dialog"""
    data = get_data_excel(filepath)
    data_sheets = data.sheet_names()
    for sheet_name in data_sheets:
        table = data.sheet_by_name(sheet_name)
        # Select specified table
        # table = data.sheet_by_index(0)
        if data: 
            # Select specified column
            col_format = ['E','F']
            try:                                              
                nrows = table.nrows                                     
                ncols = table.ncols                                         
                str_upcase = [i for i in string.ascii_uppercase]                    
                i_upcase = range(len(str_upcase))                             
                ncols_dir = dict(zip(str_upcase,i_upcase))                   
                col_index = [ncols_dir.get(i) for i in col_format] 

                for i in range(nrows):
                    Q = table.cell(i,col_index[0]).value
                    A = table.cell(i,col_index[1]).value
                    print("Q: " + Q + "\nA: " + A)
		
					# 1.分词，关键词提取
                    words = []
                    tags = []
                    words = list(jieba.cut(Q))
                    tags = jieba.analyse.extract_tags(Q, topK=10)
					# 2.语义依存树
                    semantic_trees = SemanticTree(Q)
					# 3.将每个句子的语义分析结果加入neo4j数据库
                    for semantic_tree in semantic_trees:
                        GenerateSTree(NodeClass="QA", Q=Q, A=A, words=words, tags=tags, content=semantic_tree, username="Human")
            except Exception as e:
                print('Error: %s' %e)
                return None
        else:
            print('Error! Data of %s is empty!' %sheet_name)
            return None


if __name__ == '__main__':
    handle_data_excel("./data/topic/bank/QA.xls")