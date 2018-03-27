# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from weibo.items import WeiboItem
import re,time
from scrapy.conf import settings
import pymongo

class WeiboPipeline(object):

    def parse_time(self, now_time):
        if re.match('\d+月\d+日', now_time):
            now_time=time.strftime('%Y年', time.localtime())+now_time
        if re.match('\d+分钟前', now_time):
            minute = re.match('(\d+)', now_time).group(1)
            now_time=time.strftime('%Y年%m月%d日 %H:%M', time.localtime(time.time()-float(minute)*60))
        if re.match('今天(.*)', now_time):
            now_time=re.match('今天(.*?)', now_time).group(1).strip()
            now_time=time.strftime('%Y年%m月%d日', time.localtime())+ ''+now_time

        return now_time

    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            if item['content']:
                item['content']=item['content'].lstrip(':').strip()
            if item['now_time']:
                item['now_time']=item['now_time'].strip()
                item['now_time']=self.parse_time(item['now_time'])
        return item


class MongoPipeline(object):
    def __init__(self):
        self.host=settings["MONGO_HOST"]
        self.port=settings["MONGO_PORT"]
        self.dbs=settings["MONGO_DB"]

    def open_spider(self, spider):
        self.client=pymongo.MongoClient(self.host, self.port)
        self.db=self.client[self.dbs]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.table_name].update({"id": item['id']}, {'$set': dict(item)}, True)
        return item