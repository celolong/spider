# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pymongo import MongoClient
from scrapy.conf import settings


class DoubanPipeline(object):
    def __init__(self):
        self.f = open('movie.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        print(dict(item))
        str_data = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.f.write(str_data)
        return item

    def __del__(self):
        self.f.close()


class MongoDB(object):
    def __init__(self):
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        dbname = settings['MONGO_DBNAME']
        colname = settings['MONGO_COLNAME']
        self.client = MongoClient(host=host, port=port)
        self.db = self.client[dbname]
        self.col = self.db[colname]

    def process_item(self, item, spider):
        data = dict(item)
        self.col.insert(data)
        return item

    def __del__(self):
        self.client.close()
