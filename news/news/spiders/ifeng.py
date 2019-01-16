# -*- coding: utf-8 -*-
import scrapy


class IfengSpider(scrapy.Spider):
    name = 'ifeng'
    allowed_domains = ['ifeng.com']
    # start_urls = ['http://ifeng.com/']
    start_urls = ['http://www.ifeng.com']

    # def parse(self, response):
    #     pass


    def parseOne(self, response):
        print("======",response.url)
        # print('parse_one: {0}'.format(response.url))
        links = response.xpath('//div[@class="newsList"]/ul/li/a/@href')
        # print(links)


    def parse(self, response):
        # print(response.url)
        listnum = [11490, 11528, 11574, 7609]
        for i in listnum:
            url = "http://news.ifeng.com/listpage/" + str(i) + "/0/1/rtlist.shtml"
            # print(url)
            # yield scrapy.Request(url, callback=self.parseOne)
            yield scrapy.Request(url, callback=self.parseOne)






