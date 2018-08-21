#!/usr/bin/env python3
# 感谢百度翻译，禁止用于商业用途

import requests


# 中译英
def zh2en(content):
    data = {
        'from': 'zh',
        'to': 'en',
        'query':content,
    }
    return _translate(data)


# 英译中
def en2zh(content):
    data = {
        'from': 'en',
        'to': 'zh',
        'query':content,
    }
    return _translate(data)


def _translate(data):
    # 手机版api
    url = 'http://fanyi.baidu.com/basetrans'
    headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}
    response = requests.post(url,data,headers=headers)
    result = response.json()['trans'][0]['dst']
    return result


if __name__=="__main__":
    print(zh2en('你好，世界'))
    print(en2zh('Hello, world'))
