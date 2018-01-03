# coding=utf-8
"""
author:cello
"""
import requests

if __name__ == "__main__":
    url = 'http://www.baidu.com'
    headers ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}

    responses = requests.get(url,headers)
    # responses.content直接为bytes类型
    # print(type(responses.content))
    # print(responses.content.decode())
    # # responses.text为str类型，为了防止出现乱码，在responses.text前先定义编码类型,responses.encoding='utf-8
    # print(type(responses.text))
    # print(responses.text)
    print(responses.encoding)
    responses.encoding="utf-8"
    print(responses.text)
    print(responses.encoding)


