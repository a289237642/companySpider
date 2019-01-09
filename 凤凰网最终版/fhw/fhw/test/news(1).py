# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fhw.items import FhwItem
from selenium import webdriver
from datetime import datetime
import re

PREFIX = r'Z:\\'
WEBSITE = r'ifeng'


class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/listpage/11490/20181231/1/rtlist.shtml',
                  'http://news.ifeng.com/listpage/11528/0/1/rtlist.shtml',
                  'http://news.ifeng.com/listpage/11574/0/1/rtlist.shtml',
                  'http://news.ifeng.com/listpage/7609/0/1/rtlist.shtml']

    rules = (
        Rule(LinkExtractor(allow=r'rtlist.shtml$'), callback='parse_item', follow=True),
    )

    def parse_datel(self, response):
        '''
        该方法用于处理详情页信息
        通过xpath定位出相应的数据

        '''
        print("====", response.url)
        item = FhwItem()
        # 文章标题
        title = response.xpath('//div[@class="yc_tit"]/h1/text()|//div[@id="artical"]/h1/text()').extract()
        # 文章内容
        cont = response.xpath('//div[@id="main_content"]/p/text()').extract()
        # 新闻来源
        source = response.xpath('//span[@class="ss03"]/a/text()|//div[@class="yc_tit"]/p/a/text()').extract()
        # 图片
        image_bool = response.xpath('//p[@class="detailPic"]')
        if image_bool:
            images = response.xpath('//p[@class="detailPic"]/img/@src').extract()

        item['BTIT'] = title
        item['ZWWB'] = cont
        item['XWLY'] = source
        item['TP_URL'] = response.url
        yield item

    def parse_item(self, response):
        '''
        该方法用于处理列表页
        作用是将日期为20180601以后的四个专题
        新闻列表页获取到，之后从列表页中使用
        xpath将详情页url获取到，再将详情页的url进行
        第二次清洗过滤出符合需求的详情页url，在将详情页
        的url交给parse_datel方法处理
        '''
        num = "".join(response.url).split("/")[5]
        if int(num) >= 20180601:
            # 新闻列表页
            news_list_url = response.xpath('//div[@class="newsList"]/ul')
            if news_list_url:
                news_url = response.xpath('//div[@class="newsList"]/ul/li/a/@href').extract()
                for new_url in news_url:
                    pattern = re.compile(r'^http://(.*)/a/(\d+)/(.*).shtml$')
                    datel_url = pattern.match(new_url)
                    datel_url = datel_url.group(0)
                    yield scrapy.Request(datel_url, callback=self.parse_datel, dont_filter=True)
