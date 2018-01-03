# coding=utf-8
"""
author:cello
"""
import requests
from lxml import etree
import time,os
from threading import Thread,current_thread
from queue import Queue

class TieBa(object):
    def __init__(self,name):
        self.name = name
        self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0'}
        self.next_url = 'https://tieba.baidu.com/f?ie=utf-8&kw={}&fr=search'.format(name)

    # 通过地址获取对应的xml文本内容
    def get_xml(self,urls):
        responses = requests.get(urls,headers = self.headers, timeout = 10)
        html = responses.content
        xml = etree.HTML(html) #  获取xml格式的内容
        return xml
    # 根据文本内容获取每页帖子的地址内容
    def get_href(self,xml):
        li_list = xml.xpath('//div[@class="threadlist_title pull_left j_th_tit "]')
        # 获取每个帖子的链接和标题
        for i in li_list:
            dict_url = {}
            href = i.xpath('./a/@href')[0]
            print(href)
            title = i.xpath('./a/@title')[0]
            if "高仿鞋" not in title:
                dict_url[title] = 'https://tieba.baidu.com'+href
            # 将保存的标题和链接以字典形式保存到队列中
            queue_url.put(dict_url)

    # 进入每个帖子，获取其帖子中的图片地址,并保存
    def get_page(self):
        dict_url = queue_url.get()
        for i in dict_url:
            if dict_url[i] != 0:
                print(current_thread())
                # 每页中的第一页
                next_page= dict_url[i]
                dict_url[i] = 0
                while True:
                    print(next_page)
                    print('xia:'+next_page)
                    html = self.get_xml(next_page)
                    # 获取图片地址
                    self.pic_url(html,i)
                    try:
                        # 尝试获取下一页
                        next_page = html.xpath('//li[@class="l_pager pager_theme_5 pb_list_pager"]/a[contains(text(),"下一页")]/@href')[0]
                        next_page = "https://tieba.baidu.com" + next_page
                    except Exception as f:
                        print("get_page:"+ str(f) + next_page)
                        time.sleep(10)
                        break

    # 将图片保存
    def save_pic(self,title,pic_url):
        if not os.path.exists(self.name + 'image'):
            os.makedirs(self.name + 'image')
        b_img = requests.get(pic_url,self.headers,timeout = 10 ).content
        file_name = self.name + 'image'+os.sep+pic_url.split('/')[-1]
        with open(file_name,'wb') as f:
            f.write(b_img)
            global nume
            nume += 1
            print(nume)


    # 获取每页帖子的url
    def get_urls(self):
        while True:
            xml = self.get_xml(self.next_url)
            self.get_href(xml)
            # for i in range(2):
            #     t = Thread(target=self.get_page)
            #     t.start()
            self.get_page()
            try:
                self.next_url = "http:" + xml.xpath('//a[@class="next pagination-item "]/@href')[0]
                print('下一页:'+self.next_url)
            except Exception as f:
                print("get_url:"+str(f)+self.next_url)
                break


    # 获取每页图片的图片地址，保存在字典dict_pic中
    def pic_url(self, html,title):
        urls = html.xpath('//div/img[@class="BDE_Image"]/@src')
        # 如果没有照片则退出
        if len(urls)==0:
            return
        for index, pic_url in enumerate(urls):
            self.save_pic(title,pic_url)

    def run(self):
        self.get_urls()


if __name__ == "__main__":
    nume = 0
    queue_url = Queue()
    queue_page = Queue()
    p = TieBa('美少女')
    p.run()
