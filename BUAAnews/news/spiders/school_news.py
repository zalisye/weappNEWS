# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import random
import sys

class SchoolNewsSpider(scrapy.Spider):
    name = 'school_news'
    allowed_domaims=["buaa.edu.cn"]
    start_urls = ["http://news.buaa.edu.cn/zhxw_new.htm"]

    def parse(self, response):
        for a in response.xpath('//a[re:test(@href,"^info/")]/@href').extract():
            try:
                url='http://news.buaa.edu.cn/'+a
                yield scrapy.Request(url,callback=self.parse_news)
            except:
                continue

    def parse_news(self,response):
        items=NewsItem()
        items['title']=response.xpath('//title/text()').extract()
        items['content']=response.xpath('//div[@id="vsb_content"]//p/text()').extract()
        items['time']=response.xpath('//span[@class="ri"]/text()').extract()[1].split(':')[1]
        yield items


