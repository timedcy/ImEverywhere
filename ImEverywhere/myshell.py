#!/usr/bin/env python3
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""
Manage NLU with shell
"""
from optparse import OptionParser 
 
[...]  

def myshell():  
    usage = "usage: python %prog [options] arg"  
    parser = OptionParser(usage)    
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")  
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose") 
    parser.add_option("-f", "--file", dest="filename",  
                      help="read data from filename")
    parser.add_option("-a", "--add", dest="add",  
                      help="add subgraph to graph database")
    parser.add_option("-d", "--delete", dest="delete",  
                      help="delete subgraph of graph database")
    parser.add_option("-e", "--edit", dest="edit",  
                      help="edit subgraph of graph database")
    parser.add_option("-s", "--search", dest="search",  
                      help="search subgraph of graph database")
    parser.add_option("-b", "--batch", dest="batch", action="store_true", 
                      help="batch processing of graph database")					  
    [...]  
    (options, args) = parser.parse_args()	
    if len(args) == 0:  
        parser.error("incorrect number of arguments")  
    if options.verbose:  
        print("reading %s..." % options.filename)  
    [...]  
  
if __name__ == "__main__":  
    myshell()
	