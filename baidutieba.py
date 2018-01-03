# coding=utf-8
"""
author:cello
"""
import requests

class TieBa(object):
    def __init__(self,name,page):
        self.name = name
        self.pa = int(page)
        self.url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn='.format(name)
        self.heades = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}

    def get_url(self):
        self.url_list = [self.url+str(i*self.pa) for i in range(self.pa)]

    # 保存页面
    def save(self,data, index):
        file_name = self.name + '_' + str(index)
        with open(file_name,'wb')as f:
            f.write(data)

    # 请求地址
    def run(self):
        self.get_url()
        for index, url in enumerate(self.url_list):
            responses = requests.get(url,headers=self.heades)
            self.save(responses.content, index)




if __name__ == "__main__":
    name = input('请输入查询贴吧的名字：')
    page  = input('请输入查询的从头开始几页：')
    p = TieBa(name,page)
    p.run()