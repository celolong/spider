# coding=utf-8
"""
author:cello
"""
import requests
import time
from lxml import etree
from queue import Queue
import xlwt
from threading import Thread


class WyMusic(object):
    def __init__(self):
        # 注意网易云音乐分类页面内嵌ifram，在抓包中找到http://music.163.com/discover/playlist/为正常内嵌的页面
        self.url ="http://music.163.com/discover/playlist/"
        self.headers ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
        # self.wy = xlwt.Workbook('wy.xls')
        self.type_queue=Queue()
        self.sheet_queue = Queue()
        self.music_queue = Queue()
        self.sheet_list = []
        # 创建一个列表永远存储音乐
        self.musci_list = []
        self.music_all = []


    # 获取页面信息并转换为xml格式
    def get_page(self, url):
        responses = requests.get(url,headers=self.headers,timeout = 10)
        html=  responses.content.decode()
        html = etree.HTML(html)
        return html

    # 获取歌单种类
    def get_type(self,html):
        # sheet = self.wy.add_sheet('歌曲类型')
        # sheet.write(0,0,'名字')
        # sheet.write(0, 1, '链接')
        xpath_list = html.xpath('//*[@id="cateListBox"]/div[2]/dl/dd/a')
        type_list = []
        for index,x in enumerate(xpath_list):
            type_dict = {}
            type_title = x.xpath('./@data-cat')[0]
            type_href = 'http://music.163.com'+ x.xpath('./@href')[0]
            type_dict['title'] = type_title
            type_dict['href'] = type_href
            type_dict['no'] = index+1
            type_list.append(type_dict)
            print(type_dict)
            # 将类型存入队列中
            self.type_queue.put(type_dict)
        return type_list

    # 获取所有歌单链接
    def get_music_sheet(self):
        while True:
            data = self.type_queue.get()
            sheet_url = data['href']
            # 尝试获取歌单
            try:
                # 获取歌单所有页数的链接
                while True:
                # 获取歌单界面
                    html = self.get_page(sheet_url)
                    # 获取歌单信息
                    xpath_list = html.xpath('//*[@id="m-pl-container"]/li')
                    for x in xpath_list:
                        sheet_dict = {}
                        sheet_dict['歌单名称'] = x.xpath('./p[1]/a/@title')[0]
                        sheet_dict['歌单地址'] ='http://music.163.com'+ x.xpath('./p[1]/a/@href')[0]
                        sheet_dict['歌单ower'] = x.xpath('./p[2]/a/@title')[0]
                        sheet_dict['ower地址'] ='http://music.163.com'+ x.xpath('./p[2]/a/@href')[0]
                        sheet_dict['hot'] = x.xpath('./div/div/span[2]/text()')
                        print(sheet_dict)
                        # 将歌单链接放入队列中
                        self.sheet_queue.put(sheet_dict)
                        self.sheet_list.append(sheet_dict)
                    # 歌单翻页
                    try:
                        sheet_url ='http://music.163.com'+ html.xpath('//div/a/[@class="zbtn znxt"]/@href')[0]
                        print('歌单翻页')
                    except Exception as f:
                        print(f)
                        break
            except requests.exceptions.ConnectionError:
                self.type_queue.put(data)
                print('连接有误，重新加入队列')
                break
            except Exception as f:
                print(f)
                break
            print('下一个歌单')
            self.type_queue.task_done()

    def get_music(self):
        time.sleep(2)
        while True:
            # 遍历所有歌单内容，获取歌曲
            data = self.sheet_queue.get()
            # 获取歌单界面内容
            url = data['歌单地址']
            print("--------------------------------",url)
            # 尝试获取歌曲
            try:
                html = self.get_page(url)
                xpath_list = html.xpath('//div[@id="song-list-pre-cache"]/ul/li')
                if len(xpath_list)< 1:
                    print("+++++++++++++++++++++++",data)
                else:
                    for x in xpath_list:
                        music_dict = {}
                        music_dict['歌曲'] = x.xpath('./a/text()')[0]
                        music_dict['歌曲链接'] = 'http://music.163.com' + x.xpath('./a/@href')[0]
                        # 判断是否歌曲有重复
                        if music_dict not in self.musci_list:
                            self.musci_list.append(music_dict)
                            self.music_queue.put(music_dict)
                            print(music_dict)
            except requests.exceptions.ConnectionError:
                self.sheet_queue.put(data)
                print('连接有误，重新加入队列')
                break
            except Exception as f:
                print(f)
                break
            self.sheet_queue.task_done()

    def detal_music(self):
        # 获取音乐的歌手以及专辑，名称
        while True:
            data = self.music_queue.get()
            url = data['歌曲链接']
            # http: // music.163.com / weapi / song / lyric?csrf_token = （歌词请求，为post,且需要token口令）
            # < div class ="n-cmt" id="comment-box" data-tid=R_SO_4_517567264 data-count=0 > < / div >
            # 尝试连接到页面
            try:
                html = self.get_page(url)
                str = html.xpath('//meta[@name="keywords"]/content')[0]
                sin_music = {}
                sin_music['歌手'] = str.split(',')[2]
                sin_music['专辑'] = str.split(',')[1]
                sin_music['歌名'] = str.split(',')[0]
                self.music_all.append(sin_music)
                print(sin_music)
            except requests.exceptions.ConnectionError:
                self.sheet_queue.put(data)
                print('歌曲连接有误，重新加入队列')
                break
            except Exception as f:
                print(f)
                break
            self.music_queue.task_done()

    def run(self):
        # 进入到歌曲种类页面
        url = self.url
        html = self.get_page(url)
        # 通过分类页面选取所有歌单种类链接
        type_list = self.get_type(html)
        thread_list = []
        # 对每个种类进行遍历获取歌单链接
        for t in range(3):
            t = Thread(target=self.get_music_sheet)
            thread_list.append(t)
        # self.get_music_sheet()
        # 遍历所有的歌单内容
        for t in range(3):
            t = Thread(target=self.get_music)
            thread_list.append(t)
        # self.get_music()
        # 创建守护线程
        for t in thread_list:
            t.setDaemon(True)
            t.start()

        # 监听线程是否完成
        time.sleep(3)
        for q in [self.music_queue,self.sheet_queue]:
            q.join()
        # 保存excel档案
        # self.wy.save('wy.xls')




if __name__ == "__main__":
    wy = WyMusic()
    wy.run()