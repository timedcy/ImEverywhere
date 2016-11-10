# -*- coding: utf-8 -*-
import sys
import os

# NLP tool: jieba
import jieba
import jieba.posseg
import jieba.analyse

# NLP tool: pynlpir
import pynlpir

# NLP tool: pyltp
from SemanticTree import SemanticTree
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller


def analyseJieba(question, language = "zh"):
    """
    The function 'analyseJieba' is employed to handling question text from speech recognition system.
    'jieba' is a NLP tool of Chinese natural language processing.
    Default mode is Chinese mode. You can  set language = 'en' when you want to analyse English.
    We can get the segments of sentences, keywords, postags and 'Semantic Dependency Tree'. All of these information are used to generate the search request to database.
    TODO: Add 'Semantic Dependency Tree' to the analysis result 'search_request'.
	
    """
    assert isinstance(question, str), "`question` must be a string"
    # 自定义词典
    jieba.load_userdict(os.path.split(os.path.realpath(__file__))[0] + "/data/jieba/userdic.txt")
    # 分词
    segments = jieba.cut(question)
    # The type of segments is 'generator object Tokenizer.cut'
    # Translate the generator into a list in the dialog mode instead of the long text
    dialog_segments = list(segments)
    # print('/'.join(segments))
	
    # 关键词提取
    tags = jieba.analyse.extract_tags(question, topK=10)
    # The type of tags is 'list'
    # print(",".join(tags))
	
    # 词性标注
    poss = jieba.posseg.cut(question)
    # The type of poss is 'generator object cut'
    # Translate the generator into a list in the dialog mode instead of the long text
    dialog_poss = []
    for w in poss:
        # print(w.word, "\t", w.flag)
        dialog_poss.append((w.word, w.flag))
	
    # 语义依存树
    dialog_sTree = None
        
    search_request = dict(segments = dialog_segments, words = dialog_poss, keywords = tags, sTree = dialog_sTree)
    return search_request
	
def analyseLtp(question, language = "zh"):
    """
    The function 'analyseLtp' is employed to handling question text from speech recognition system.
    'Ltp' is a NLP tool of Chinese natural language processing.
    Default mode is Chinese mode. You can  set language = 'en' when you want to analyse English.
    We can get the segments of sentences, keywords, postags and 'Semantic Dependency Tree'. All of these information are used to generate the search request to database.
    TODO: Support SemanticTree now. Then add local 'Semantic Dependency Tree' to the analysis result 'search_request'.
	
    """
    # 分句，分词-支持分词外部自定义词典与个性化分词模型
    # paragraph = "我想买一张明天上海到北京的机票。请问您能帮我订票吗？"
    # question = SentenceSplitter.split(paragraph)[0]
    segmentor = Segmentor()
    segmentor.load(os.path.split(os.path.realpath(__file__))[0] + "/data/ltp/cws.model")
    segments = segmentor.segment(question)
    # The type of segments is 'generator object Tokenizer.cut'
    # Translate the generator into a list in the dialog mode instead of the long text
    dialog_segments = list(segments)
    print(len(dialog_segments))
    print("\t".join(segments))
	
    # 词性标注-支持自定义词典
    postagger = Postagger()
    postagger.load(os.path.split(os.path.realpath(__file__))[0] + "/data/ltp/pos.model")
    postags = postagger.postag(segments)
    poss = list(postags)
    print(len(poss))
    print("\t".join(postags))
    # 合并(分词，词性)二元组列表
    dialog_poss = []
    for index in range(len(dialog_segments)):
        dialog_poss.append((dialog_segments[index], poss[index])) 
		
    # 依存句法分析	
    parser = Parser()
    parser.load(os.path.split(os.path.realpath(__file__))[0] + "/data/ltp/parser.model")
    arcs = parser.parse(segments, postags)
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
	
    # 命名实体识别
    recognizer = NamedEntityRecognizer()
    recognizer.load(os.path.split(os.path.realpath(__file__))[0] + "/data/ltp/ner.model")
    netags = recognizer.recognize(segments, postags)
    value = list(netags)
    tags = []
    for index in range(len(value)):
        if value[index] != "O":
            tags.append(dialog_segments[index])
    # print(tags)
    # print("\t".join(netags))

    # 语义角色标注
    labeller = SementicRoleLabeller()
    labeller.load(os.path.split(os.path.realpath(__file__))[0] + "/data/ltp/srl/")
    roles = labeller.label(segments, postags, netags, arcs)
    for role in roles:
        print(role.index, "".join(
		    ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

    # 释放模型
    segmentor.release()
    postagger.release()
    parser.release()
    recognizer.release()
    labeller.release()
	
    # 语义依存树-目前只支持语言云	
    # 可以与其他分析过程多线程实现以提升速度
    sdp_content = SemanticTree(question)
    # sdp_content是一个语义树切词字典列表，包含id, cont, pos, semparent, semrelate这5个属性
        
    search_request = dict(keywords = tags, sTree = sdp_content)
    return search_request
	
def analyseNlpir(question, language = "zh"):
    """
    The function 'analyseNlpir' is employed to handling question text from speech recognition system.
    'Nlpir' is a NLP tool of Chinese natural language processing.
    Default mode is Chinese mode. You can  set language = 'en' when you want to analyse English.
    We can get the segments of sentences, keywords, postags and 'Semantic Dependency Tree'. All of these information are used to generate the search request to database.
    TODO: Add 'Semantic Dependency Tree' to the analysis result 'search_request'.
	
    """
    pynlpir.open()
	
    # 分词+词性标注
    segments = pynlpir.segment(question)
    # segments = pynlpir.segment(question, pos_names='all', pos_english=False)
    # The type of segments is 'list'
    # print(segments)
    dialog_segments = []
    for segment in segments:
        # print(segment[0], '\t', segment[1])
        dialog_segments.append(segment[0])
	
    # 关键词提取
    tags = pynlpir.get_key_words(question, weighted=True)
    # The type of tags is 'list'
    # for tag in tags:
        # print(tag[0], '\t', tag[1])
	
    # 语义依存树	
    dialog_sTree = None
		
    search_request = dict(segments = dialog_segments, words = segments, keywords = tags, sTree = dialog_sTree)
	
    pynlpir.close()	
    return search_request
