# -*- coding: UTF-8 -*-
"""
Batch delete subgraph in Neo4j.
"""
import sys
from os import getenv
from py2neo import Graph


def delete(name=None, pattern="-n"):     
    """
    You can use 'Python3 delete.py -[all n r nr rm nrm] namelist'
	
    """
    graph = Graph("http://localhost:7474/db/data", password=getenv("GQY_PASSWORD"))
    if pattern == "-all":
        graph.delete_all()
    elif pattern == "-n":
        graph.run("MATCH(n:" + name + ") DETACH DELETE n")
    elif pattern == "-r":
        graph.run("MATCH (n)-[r:" + name + "]-(m) DETACH DELETE r")
    elif pattern == "-nr":
        graph.run("MATCH (n)<-[r:" + name + "]-(m) DETACH DELETE r DELETE n")
    elif pattern == "-rm":
        graph.run("MATCH (n)-[r:" + name + "]->(m) DETACH DELETE r DELETE m")
    elif pattern == "-nrm":
        graph.run("MATCH (n)-[r:" + name + "]-(m) DETACH DELETE r DELETE n DELETE m")

def main():
    assert len(sys.argv) >= 2
    print(sys.argv)
    pattern = sys.argv[1]
    if pattern == "-all":
        delete(name="all", pattern=pattern)
    for name in sys.argv[2:]:
        delete(name=name, pattern=pattern)

if __name__ == "__main__":
    main()