# coding=utf-8
"""
author:cello
"""

import requests
from lxml import etree
import json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
url = 'http://zhaopin.baidu.com/api/quanzhiasync?query=%E7%88%AC%E8%99%AB&city=%E6%B7%B1%E5%9C%B3&rn=100&pn=100'
reponsers = requests.get(url,headers=headers)
html =reponsers.content.decode(encoding='utf-8')
html = json.loads(html)

print(html)
# html = etree.HTML(html)
# print(etree.tostring(html))
# list = html.xpath('//script[4]')

# for x in list:
#     a = x.xpath('./a/text()')[0]
#     b = 'http://music.163.com' + x.xpath('./a/@href')[0]
#     # c= x.xpath('./td[4]/div[@class="text"]/@title')[0]
#     # d = 'http://music.163.com' + x.xpath('./td[4]/a/@href')[0]
#     # e= html.xpath('./td[5]/a/@title')[0]
#     # f = 'http://music.163.com' + x.xpath('./td[5]/a/@href')[0]
#     print(a)
#     print(b)
    # print(c)
    # print(d)
    # print(e)
    # print(f)

