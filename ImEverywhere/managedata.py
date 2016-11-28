#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neo4j图形数据库管理
1.支持节点，关系，子图，全图的增、删、改、查
2.支持批处理
3.支持命令行
4.支持读取数据文件批量导入及导出为需要的文件格式
"""
import sys
import json
import codecs
from mytools import time_me, get_data_excel
from py2neo import Graph, Node, Relationship
from semantic import synonym_cut, generate_qa

# Read config
config = {}
with codecs.open("../config.json","rb","UTF-8") as f:
	config = json.loads(f.read())
# Set up a link to the local graph database.
graph = Graph("http://localhost:7474/db/data", password=config["password"])

# edit		
# graph = Graph("http://localhost:7474/db/data", password="gqy")
# node=graph.find_one("SynonymTag", "name", "Ca03A03#")
# node["words"].remove("有效期")
# node["words"].remove("能用多久")
# graph.push(node)	

	
@time_me()
def generate_synonym(tag=None, words=None):
    """
    在图形数据库 neo4j 里建立 Synonym 同义词关系图
    1.SynonymTag 为标签节点，以 name 属性建立索引
    2.hot 为搜索热度，pos 为词性，vec为 word2vec 训练后的词向量
    """
    assert isinstance(tag, str), "The tag of synonyms must be a string."
    assert words is not None, "The words can not be None."
    tag_node = graph.find_one("SynonymTag", "name", tag)
    if tag_node:
        synonym_root = tag_node
        new_words = list(set(words).difference(set(synonym_root["words"])))
        synonym_root["words"].extend(new_words)
        graph.push(synonym_root)
    else:
        synonym_root = Node("SynonymTag", name=tag, cname="", words=words, pos="", hot=0)
        new_words = words
    for word in new_words:
        synonym_node = Node("Synonym", name=word, tag=tag, pos="", vec=[], hot=0)
        relationship = Relationship(synonym_root, "contain", synonym_node)
        graph.create(relationship)

			
@time_me()		
def add_to_synonym(sample=None, words=None):     
    """
    Add a new synonym word to database.
    """
    assert isinstance(sample, str), "The sample word must be a string."
    assert words is not None, "The new words can not be None."	
    sample_node = graph.find_one("Synonym", "name", sample)
    if sample_node:
        generate_synonym(sample_node["tag"], words)
    else:
        print("Sorry, can't find SynonymTag, please create SynonymTag first!")

def handle_data_excel(filepath):
    """Processing data of excel"""
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
					# Your processing function of excel data here
                    add_qa(Q, A, delimiter="|")
					
            except Exception as e:
                print('Error: %s' %e)
                return None
        else:
            print('Error! Data of %s is empty!' %sheet_name)
            return None

def add_qa(Q, A, delimiter = None):
    qlist = Q.split(delimiter)
    alist = A.split(delimiter)
    for q in qlist:
        words = synonym_cut(q, 'w')	
        tags = synonym_cut(q, 't')	
        generate_qa(NodeClass="QA", Q=q, A=alist, words=words, tags=tags, username="Human")
	
@time_me(format="ms")	
def test_add_qa():
    handle_data_excel("./data/train.xls")		

def test_add_to_synonym():
    assert len(sys.argv) >= 2
    print(sys.argv)
    add_to_synonym(sample=sys.argv[1], words=sys.argv[2:])
		
		
def test_generate_synonym():
    tag = ""
    words = []
    if len(sys.argv) >= 2:
        generate_synonym(tag=sys.argv[1], words=sys.argv[2:])
    # else:
        # with open("data/synonym.txt", encoding="UTF-8") as file:
            # for line in file:
                # content = line.split()
                # print(content)
                # generate_synonym(content[0], content[1:])
	
	
def test_generate_dict():
    with open("data/synonymdict.txt", 'w', encoding="UTF-8") as new:
        with open("data/synonym.txt", 'r', encoding="UTF-8") as file:
            for line in file:			
                content = line.split()
                for word in content[1:]:
                    new.write(word + " 2000 " + content[0] + "\n")
    				

if __name__ == "__main__":
    # TODO: Add pattern
	# test_add_qa()
    # test_add_to_synonym()
    # test_generate_synonym()
    test_generate_dict()
