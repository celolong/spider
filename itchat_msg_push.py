# coding=utf-8
"""
author:cello
"""
import requests,itchat
from lxml import etree
import time

class Choushi(object):
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
        self.url = 'https://www.qiushibaike.com'

    def get_page(self,url):
        responses = requests.get(url,self.headers,timeout = 5)
        content = responses.content
        xml = etree.HTML(content)
        return xml

    def get_urls(self,xml):
        # 获取div列表
        div_list= xml.xpath('//a[@class="contentHerf"]/@href')
        url_list = []
        for i in div_list:
            # 获取里面的内容地址
            url_list.append(i)
        return url_list

    def run(self):
        url = self.url + '/text/'
        xml = self.get_page(url)
        url_list = self.get_urls(xml)
        for ur in url_list:
            url = self.url + ur
            xml = self.get_page(url)
            content = self.get_content(xml,ur)

    def get_content(self, xml,ur):
        cont = xml.xpath('//div[@class="content"]')
        if len(cont) > 0:
            content = cont[0].xpath('string(.)')
            print(content)
            dict[ur] = content
            return content
        else:
            pass

if __name__ == "__main__":
    dict = {}
    choushi = Choushi()
    choushi.run()
    itchat.auto_login(enableCmdQR=False, hotReload=True)
    text =itchat.get_chatrooms(update=True)
    print(text)
    tt = itchat.search_chatrooms(name="ps小能手")
    print(tt)
    friend = itchat.search_friends(name='胡华康')
    print(friend)
    friend_id = friend[0]["UserName"]
    print(friend_id)
    chat_id = tt[0]["UserName"]
    print(chat_id)
    h = 10
    for i in dict:
        while True:
            dt = list(time.localtime())
            hour = dt[3]
            minute = dt[4]
            time.sleep(5)
            print(hour,minute)
            if minute == 00:
                msgs = "celo为你报时,现在时间为："+ str(hour)+":00----给你一个糗事，要笑口常开哦(这不是骚扰，这不是骚扰!)："  + dict[i]
                itchat.send(msg=msgs,toUserName=friend_id)
                time.sleep(60)
                h=1
                break


