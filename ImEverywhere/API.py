#!/usr/bin/env python3
# -*- coding:utf8 -*-

import csv
	
def topic_query(topic=None, parameters=None):
    """
    话题查询API，当参数topic为None时是普通聊天，parameters为None时获取默认信息
    从参数切分属性，主属性即行属性，副属性即列属性，据此查找矩阵中的值
    若有行属性或者列属性为空则说明有上下文的省略语义，在传入参数之前会进行上下文的处理，将记忆参数也附加进去
    """
    assert topic is not None, "topic cannot be None"
    result = []
    keys = []
    data = "data/topic/" + topic + "/test.csv"
	# 参数切分为行属性keys与列属性items
    with open(data) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['key'] in parameters:
                keys.append(row['key']) 
        items = list(set(parameters).difference(set(keys)))
    with open(data) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in keys:
                if key == row["key"]:
                    if items:
                        for item in items:
                            result.append(item + key + row[item])
                    else:
                        result.append(key + row["default"])
    return ";".join(result)
	
if __name__ == '__main__':
    answer = topic_query(topic="weather", parameters=["广东", "北京", "明天", "后天"])
    print(answer)