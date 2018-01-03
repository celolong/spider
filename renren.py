# coding=utf-8
"""
author:cello
"""
import requests
import re

if __name__ == "__main__":

    # cookies的使用
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    # responses = requests.get('http://baidu.com',headers=headers)
    # cookiejar = responses.cookies
    # print(cookiejar)
    # print(type(cookiejar))
    # cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
    # print(cookiedict)
    # print(len(cookiedict))
    # print(requests.utils.cookiejar_from_dict(cookiedict))

    # session的使用
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    # 创建session实例对象
    session = requests.session()
    data = {'email':'747543777@qq.com','password':'woairenren'}
    # responses = requests.get('http://www.renren.com/PLogin.do',headers=headers,data=data)
    session.post('http://www.renren.com/PLogin.do',data=data)
    responses = session.get('http://www.renren.com')
    print(responses.status_code)
    print(session)
    print(re.findall('陈龙',responses.content.decode()))