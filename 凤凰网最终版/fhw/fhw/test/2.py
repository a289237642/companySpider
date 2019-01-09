# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fhw.items import FhwItem


class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/daohang']
    rules = (
        Rule(LinkExtractor(allow=r'a/(\d+)/(\d+)_(\d+).shtml'), callback='parse_item', follow=True),
    )

    # 处理url
    def strUrl(self, str):
        str1 = str.split("/")[4]
        return str1

    def parse_item(self, response):
        print("===============>", response.url)
        # a = self.strUrl(response.url)
        # if int(a) >= 20180601:
        # print("====>>>>", response.url)
        # if len(response.xpath('//div[@class="theLogo"]/div/a[2]/text()')) > 0:
        #     tagKey = response.xpath('//div[@class="theLogo"]/div/a[2]/text()').extract()[0]
        #     print(tagKey)
        # if tagKey == "国际" or tagKey == "大陆" or tagKey == "台湾" or tagKey == "港澳":
        #     print(tagKey)
        #     if len(response.xpath('//h1[@id="artical_topic"]/text()')) > 0:
        #         BT = response.xpath('//h1[@id="artical_topic"]/text()').extract()[0]
        # print(BT)
