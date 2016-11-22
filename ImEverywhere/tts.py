#/usr/bin/env python3
#coding=utf8

import uuid
import json
import langid
import time
import pygame.mixer
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
from urllib.error import URLError, HTTPError


def get_token(app_key, secret_key):
    url_get_base = "https://openapi.baidu.com/oauth/2.0/token"
    url = url_get_base + "?grant_type=" + "client_credentials" + "&client_id=" + app_key + "&client_secret=" + secret_key
    response = urlopen(url)
    response_text = response.read().decode("utf-8")
    json_result = json.loads(response_text)
    return json_result['access_token']
	
# Pre initialized to accelerate the 'tts_baidu'
pygame.mixer.init()
key = "QrhsINLcc3Io6w048Ia8kcjS"
secret_key = "e414b3ccb7d51fef12f297ffea9ec41d"
access_token = get_token(key, secret_key)
mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]	


def tts_baidu(info, language='zh'):     
    assert isinstance(info, str), "Info must be a string"	
	
    url_get_base = "http://tsn.baidu.com/text2audio"
    # key = "QrhsINLcc3Io6w048Ia8kcjS"
    # secret_key = "e414b3ccb7d51fef12f297ffea9ec41d"
    # access_token = get_token(key, secret_key)
    # mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    url = url_get_base + '?tex=' + quote(info) + '&lan=zh&vol=9&cuid=' + mac_address + '&ctp=1&tok=' + access_token
    try:
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
        filename = "log/temp_" + current_time + ".mp3"
        response = urlopen(url)
        f = open(filename, "wb")
        f.write(response.read())
        f.close()
		
        # pygame.mixer.init()
        track = pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        # pygame.mixer.music.set_volume(6.0)
        # time.sleep(5)
        # pygame.mixer.music.stop()		
    except Exception as e:
        print(e)
	

if __name__ == "__main__":
	print("进入语音合成模式 Enter the TTS mode...") 
	
	# Interaction test in 'Local'
    # Automatic language detection, the default tts_baidu mode is 'zh' represents Chinese
	while True:
		try:
			question = input(">>")
			inputLang = langid.classify(question)[0]
			tts_baidu(question, language=inputLang)
		except KeyboardInterrupt:
			break

    # Word test with 'Travis CI'	
	question = "和您聊天真开心"
	print("question: " + question)
	print("You can hear... ")
	tts_baidu(question, language="zh")
