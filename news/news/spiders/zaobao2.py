# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news.items import ZaoBaoItem


class ZaoBaoSpider(CrawlSpider):
    name = 'zaobao2'
    allowed_domains = ['zaobao.com']
    start_urls = ['http://www.zaobao.com']

    rules = (
        # Rule(LinkExtractor(allow=r'/realtime/china/story\d{8}-\d{6}'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/realtime/china/story20190105-\d{6}'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 把响应内容写入文件 response.body 是 bytes 类型
        # filename = response.url.split("/")[-1] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        url = response.url
        print(type(response.body))



        print(url)
        o = urlparse(url)
        print(o.path)
        title = response.xpath('//meta[@property="og:title"]/@content').extract_first()

        i = ZaoBaoItem()
        i['title'] = title
        return i

    def get_lmlj(self):
        pass
