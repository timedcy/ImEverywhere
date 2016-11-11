#!/usr/bin/env python3
# -*- coding:utf8 -*-

import asr as sr
from tts import ttsBaidu
from QA import SearchDatabase, UnderstandContext

r = sr.Recognizer()
m = sr.Microphone(1, 16000, 2048)

if __name__ == '__main__':
    answer = ""	
    print("A moment of silence, please...")
    with m as source:
        r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            print("Say something!")
            audio = r.listen(source)
            try:
                # step 1.ASR with Baidu REST API 
                sentence = r.recognize_baidu(audio)
				# step 2.NLP and Deep Learning
                if sentence == 'err_msg':
                    answer == "对不起我没听清您说的话，请问可以再重复一遍吗？"
                else:
				    # 基于语义模式匹配
                    answer = SearchDatabase(question=sentence, username="Human")
					# 基于上下文理解
                    # answer = UnderstandContext(question=sentence, username="user1")
				# step3.TTS with Baidu REST API
                print("A: " + answer)
                ttsBaidu(answer, language="zh")            
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Baidu Speech Recognition service; {0}".format(e))
				