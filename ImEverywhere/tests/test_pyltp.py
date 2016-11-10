#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

paragraph = '中国进出口银行中国银行加强合作。中国进出口银行中国银行加强合作！'
# paragraph = '我想买一张明天上海到广州的机票。我想买一张明天上海到广州的机票！'
sentence = SentenceSplitter.split(paragraph)[0]

segmentor = Segmentor()
segmentor.load("../data/ltp_data/cws.model")
words = segmentor.segment(sentence)
print(words)
print("\t".join(words))

postagger = Postagger()
postagger.load("../data/ltp_data/pos.model")
postags = postagger.postag(words)
# list-of-string parameter is support in 0.1.5
# postags = postagger.postag(["中国","进出口","银行","与","中国银行","加强","合作"])
print("\t".join(postags))

parser = Parser()
parser.load("../data/ltp_data/parser.model")
arcs = parser.parse(words, postags)
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

recognizer = NamedEntityRecognizer()
recognizer.load("../data/ltp_data/ner.model")
netags = recognizer.recognize(words, postags)
print("\t".join(netags))

labeller = SementicRoleLabeller()
labeller.load("../data/ltp_data/srl/")
roles = labeller.label(words, postags, netags, arcs)

for role in roles:
    print(role.index, "".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

segmentor.release()
postagger.release()
parser.release()
recognizer.release()
labeller.release()
