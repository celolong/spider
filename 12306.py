# coding=utf-8
"""
author:cello
"""
import requests
import re

if __name__ == "__main__":
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    responses = requests.get('http://www.12306.cn/mormhweb/',verify=False)
    print(responses.content.decode())