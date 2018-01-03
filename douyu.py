# coding=utf-8
"""
author:cello
"""
import xlwt
from selenium import webdriver
import json,time
from threading import Thread
from queue import Queue

class Douyu(object):
    # 导入selenium 模块，以及相应初始化
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.url = 'https://www.douyu.com/directory/all'
        # 将数据保存到json文件中
        self.file = open('douyu.json','w',encoding='utf-8')
        self.queue_data = Queue()
        self.queue_xls = Queue()
        self.xls = xlwt.Workbook('douyu.xls')
        self.dt = time.localtime()

    # 创建xls中sheet以及标题
    def cxls(self):
        self.sheets = self.xls.add_sheet('数据%s-%s-%s-%s'%(self.dt[1],self.dt[2],self.dt[3],self.dt[4]))
        self.sheets.write(0,0,"no")
        self.sheets.write(0, 1, "user")
        self.sheets.write(0, 2, "title")
        self.sheets.write(0, 3, "type")
        self.sheets.write(0, 4, "viewer")
        self.sheets.write(0, 5, "img")
        self.sheets.write(0, 6, "href")
        self.sheets.write(0, 7, "room_id")

    # 将数据添加进excel
    def wxls(self):
        data_list = self.queue_xls.get()
        for index,data in enumerate(data_list):
            self.sheets.write(int(data['no']),0,data['no'])
            self.sheets.write(int(data['no']), 1, data['user'])
            self.sheets.write(int(data['no']), 2, data['title'])
            self.sheets.write(int(data['no']), 3, data['type'])
            self.sheets.write(int(data['no']), 4, data['viewer'])
            self.sheets.write(int(data['no']), 5, data['img'])
            self.sheets.write(int(data['no']), 6, data['href'])
            self.sheets.write(int(data['no']), 7, data['room_id'])
        self.queue_xls.task_done()



    def get_nodelist(self):
        # 寻找每页中的直播列表,用elements
        node_list = self.driver.find_elements_by_xpath('//*[@id="live-list-contentbox"]/li')
        # 将列表遍历，获取里面的内容
        data_list = []
        for node in node_list:
            try:
                temp = {}
                global number
                number += 1
                temp['no'] = number
                temp['title'] = node.find_element_by_xpath('./a/div/div/h3').text
                temp['type'] = node.find_element_by_xpath('./a/div/div/span').text
                temp['user'] = node.find_element_by_xpath('./a/div/p/span[1]').text
                temp['viewer'] = node.find_element_by_xpath('./a/div/p/span[2]').text
                # 注意使用selenium中xpath获取节点属性值应该用方法get_attribute()
                temp['img'] = node.find_element_by_xpath('./a/span/img').get_attribute('data-original')
                temp['href'] = 'https://www.douyu.com' + node.find_element_by_xpath('./a').get_attribute('href')
                temp['room_id'] = node.find_element_by_xpath('./a').get_attribute('data-rid')
                data_list.append(temp)
                print(number, temp)
            except Exception as f:
                print('nodelist:',f)
        return data_list


    def save(self):
        data_list = self.queue_data.get()
        for data in data_list:
            # 将pyhon中字典转换为json中的字符串,并转行
            j_data = json.dumps(data,ensure_ascii=False) + ",\n"
            self.file.write(j_data)
        self.queue_data.task_done()

    def __del__(self):
        # self.driver.close()
        self.file.close()

    def run(self):
        # 构建浏览器对象
        self.driver.get(self.url)
        self.cxls()
        while True:
            data_list = self.get_nodelist()
            self.queue_data.put(data_list)
            self.queue_xls.put(data_list)
            # 将获取的数据进行处理保存
            # self.save()
            # 使用多线程处理数据
            # 创建线程池
            thread_list = []
            for t in range(3):
                t = Thread(target=self.save)
                thread_list.append(t)
            for t in range(3):
                t = Thread(target=self.wxls)
                thread_list.append(t)
            # 设置守护进程并开启线程
            for t in thread_list:
                t.setDaemon(True)
                t.start()
            # 这里self.queue_data的join方法在等待self.queue_data中的task_done方法（如果为空则返回消息，join方法执行，由于机制为根据put是否为空）
            for q in [self.queue_data,self.queue_xls]:
                q.join()
            try:
                # 进行翻页动作
                next_page = self.driver.find_element_by_xpath('//a[@class="shark-pager-next"]')
                next_page.click()
                print('下一页')
                time.sleep(3)
            except Exception as f:
                print(f)
                break
        self.xls.save('douyu.xls')

if __name__ == '__main__':
    number = 0
    douyu = Douyu()
    douyu.run()