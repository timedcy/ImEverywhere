# -*- coding: utf-8 -*-

import nltk
from nltk import load_parser

cp = load_parser('grammars/book_grammars/sql0.fcfg')
query = 'What cities are located in China'
tokens = query.split()
for tree in cp.parse(tokens):
    print(tree)