#!/usr/bin/env python3
# -*- coding:utf8 -*-
import sys
import asr as sr
from tts import tts_baidu
from qa import search_database, understand_context
from mytools import get_current_time, change_known_hosts

r = sr.Recognizer()
m = sr.Microphone(1, 16000, 2048)

def test_txt():
    current_user = "Human"
	
    print("QA测试......") 
    filename = "log/QA_" + get_current_time() + ".md"
    f = open(filename, "w")
    f.write("标签：测试文档\n#QA测试：\n>Enter the QA mode...\n")
    while True:
        try:
            sentence = input("\n>>")
			# 基于语义模式匹配
            answer = search_database(question=sentence, username=current_user)
			# 基于上下文理解
            # answer = understand_context(question=sentence, username=current_user)
            print("R: " + answer)			
            f.write("`>>" + sentence + "`\n")
            f.write("`" + "A: " + answer + "`\n")
        except KeyboardInterrupt:
            f.close()

def test_asr():
    current_user = "Human"
    answer = ""	
    print("A moment of silence, please...")
    with m as source:
        r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            print("\nSay something!")
            audio = r.listen(source)
            try:
                # step 1.ASR with Baidu REST API 
                sentence = r.recognize_baidu(audio)
                print(">>" + sentence)
				# step 2.NLP and Deep Learning
                if sentence == 'err_msg':
                    answer == "对不起我没听清您说的话，请问可以再重复一遍吗？"
                else:
				    # 基于语义模式匹配
                    answer = search_database(question=sentence, username=current_user)
					# 基于上下文理解
                    # answer = understand_context(question=sentence, username="user1")
				# step3.TTS with Baidu REST API
                print("A: " + answer)
                tts_baidu(answer, language="zh")            
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Baidu Speech Recognition service; {0}".format(e))
				
if __name__ == '__main__':
    change_known_hosts("gqy")
    assert len(sys.argv) >= 1
    print(sys.argv)
    pattern = sys.argv[1]
    if pattern == "txt":
        test_txt()
    elif pattren == "asr":
        test_asr()	
				