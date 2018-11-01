# -*- coding: utf-8 -*-
import scrapy


class ImagelistSpider(scrapy.Spider):
    name = 'imageList'
    allowed_domains = ['image.baidu.com']
    start_urls = ['http://image.baidu.com/']

    def parse(self, response):
        print(response.text)
