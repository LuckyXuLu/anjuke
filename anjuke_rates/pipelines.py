# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import json


class AnjukeRatesPipeline(object):
    def open_spider(self, spider):  # 在爬虫启动的时候,仅执行一次

        # 创建MongoDB链接对象,绑定的数据库/集合,并保存
        client = MongoClient(host="127.0.0.1", port=27017)
        self.collection = client["anjuke"]["anjuke_rates"]

        self.counters_id = client['anjuke']
        # coltion.loadServerScripts()

    def close_spider(self, spider):  # 在爬虫关闭的时候,仅执行一次
        pass

    def process_item(self, item, spider):
        # self.collection.insert(item)

        # 自定义增长id
        item["_id"] = int(self.counters_id.eval('getNextSequence("userid")'))
        self.collection.insert(item)
        # print(item)
        return item
