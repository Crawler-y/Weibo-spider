# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Field,Item


class WeiboItem(Item):
    # define the fields for your item here like:
    table_name='weibo'


    id=Field()
    url=Field()
    content=Field()
    transmit=Field()
    comment=Field()
    assist=Field()
    now_time=Field()
    user=Field()
