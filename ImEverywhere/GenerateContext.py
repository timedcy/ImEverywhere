#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# PEP 8 check with Pylint
"""
Generate Context with neo4j.
Py2neo is a python package of neo4j, the most useful graph database.
"""
import sys
from py2neo import Graph, Node, Relationship

def generate_context(content, pattern):
    """
    在图形数据库neo4j里建立上下文关系图，对选中的节点进行扩展，组织层级
    memory为在上下文语境中的涉及的话题记忆列表
    hot为话题或者话题之间Then关系的热度，可以看出哪些话题经常关联在一起
    """
    graph = Graph("http://localhost:7474/db/data/", password="gqy")
    nodename = content[0]
    relationship = content[1]
    items = content[2:]
    context_type = dict(t="topic", c="topic", u="User")
    if pattern == "t" or pattern == "u":
        node = Node(context_type[pattern], name=nodename, items=items, \
            memory_from=[], memory_to=[], memory_tags=[], hot=0)
        graph.create(node)
    if pattern == "c" or pattern == "u":
        node_from = graph.find_one(context_type[pattern], "name", nodename)
        for item in items:
            node_to = graph.find_one("topic", "name", item)
            from_to = Relationship(node_from, relationship, node_to, hot=0)
            graph.create(from_to)

def main():
    """
    测试，命令行构建，默认构建顺序为t-c-u
    """
    assert len(sys.argv) >= 2
    print(sys.argv)
    pattern = sys.argv[1]
    filepath = "./data/topic/"
    filename = dict(t="topic.txt", c="context.txt", u="user.txt")
    with open(filepath + filename[pattern], encoding="UTF-8") as file:
        for line in file:
            if line != "\n":
                print(line)
                generate_context(line.split(), pattern)

if __name__ == '__main__':
    main()
	