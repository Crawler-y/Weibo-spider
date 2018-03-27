# -*- coding: utf-8 -*-
import scrapy
import re
from weibo import items
from scrapy_redis.spiders import RedisSpider

class WeibosSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    search_url='https://weibo.cn/search/mblog'
    max_page=100

    def start_requests(self):
        keyword='刘德华'
        url='{url}?keyword={keyword}'.format(url=self.search_url, keyword=keyword)
        for i in range(self.max_page+1):
            data={
                "mp":str(self.max_page),
                "page":str(i),
            }
            yield scrapy.FormRequest(url, formdata=data, callback=self.all_page)

    def all_page(self, response):
        wb=response.xpath('//div[@class="c" and contains(@id, "M_")]')
        for node in wb:
            if bool(node.xpath("./div/span[@class='cmt']").extract_first()):
                detail_url=node.xpath('./div/a[contains(., "原文评论[")]/@href').extract_first()
                print(detail_url, "详细内容url")
            else:
                detail_url=node.xpath('./div/a[contains(., "评论[")]/@href').extract_first()
                print(detail_url, "详细内容url")
            yield scrapy.Request(detail_url, callback=self.get_content)


    def get_content(self, response):
        url=response.url
        id=re.search('comment\/(.*?)\?',response.url).group(1)
        content=','.join(response.xpath('//div/span[@class="ctt"]/text()').extract()).replace('\u200b','').replace('\u3000','')

        transmit = response.xpath('//span/a[contains(., "转发[")]/text()').re_first('转发\[(.*?)\]')
        comment=response.xpath('//span[@class="pms" and contains(., "评论[")]/text()').re_first('评论\[(.*?)\]')
        assist=response.xpath('//a[contains(., "赞[")]/text()').re_first('赞\[(.*?)\]')

        now_time=response.xpath('//span[@class="ct"]/text()').extract_first()
        user = response.xpath('//div[@id="M_"]/div[1]/a/text()').extract_first()
        weibo = items.WeiboItem()
        for field in weibo.fields:
            try:
                weibo[field] = eval(field)
            except NameError:
                self.logger.debug('Field Not Defind'+field)
        yield weibo

