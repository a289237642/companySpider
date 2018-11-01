# -*- coding: utf-8 -*-
import scrapy


class ImagelistSpider(scrapy.Spider):
    name = 'imageList'
    allowed_domains = ['image.baidu.com']
    start_urls = ['https://image.baidu.com/search/index?']
    keyword = input("")

    data = {

    }

    def parse(self, response):
        print(response.text)
