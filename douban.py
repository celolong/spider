# coding=utf-8
"""
author:cello
"""
import requests,json


class  Douban(object):
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
        self.url = "https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?start=0&count=50"
    # 打开地址，获取json数据,这里用手机端比较容易获取
    def get_data(self):
        responses = requests.get(self.url,headers = self.headers)
        # 获取的内容为bytes类型
        print(responses.content)
        return responses.content.decode()

    def get_parse(self,data):
        # 将json转换为python中的字典
        dict_data = json.loads(data)
        print(type(dict_data))
        move_list = dict_data["subject_collection_items"]
        data_list=[]
        for i in move_list:
            temp = {}
            temp['name'] = i["title"]
            temp['url']= i['url']
            data_list.append(temp)
        return data_list

    def save(self,data_list):
        with open('move.json','wb') as f:
            for data in data_list:
                str_data = json.dumps(data,ensure_ascii=False) + ',\n'
                f.write(str_data.encode())

    def run(self):
        data = self.get_data()
        print(type(data))
        data_list = self.get_parse(data)
        print(data_list)
        self.save(data_list)

if __name__ == "__main__":
    douban =Douban()
    douban.run()