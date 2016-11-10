#!/usr/bin/env python3
# -*- coding:utf8 -*-

from QA import SearchDatabase, UnderstandContext

if __name__ == '__main__':	
    current_user = "user1"
	
    print("QA测试......") 
    filename = "log/QA_" + time.strftime("%Y-%m-%d-%H-%M",time.localtime(time.time())) + ".md"
    f = open(filename, "w")
    f.write("标签：测试文档\n#QA测试：\n>Enter the QA mode...\n")
    while True:
        try:
            sentence = input("\n>>")
			# 基于语义模式匹配
            # answer = SearchDatabase(question=sentence, username=current_user)
			# 基于上下文理解
            answer = UnderstandContext(question=sentence, username=current_user)
            print("A: " + answer)            
            f.write("`>>" + sentence + "`\n")
            f.write("`" + "A: " + answer + "`\n")
        except KeyboardInterrupt:
            f.close()
			