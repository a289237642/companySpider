# -*- coding: utf-8 -*-

from sick.items import SickItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider


class SicklistSpider(RedisCrawlSpider):
    name = 'sickList'
    allowed_domains = ['ask.39.net']
    start_urls = ['http://ask.39.net']

    # scrapy-redis
    redis_key = 'myspider:start_urls'
    # 规则爬虫
    rules = (
        Rule(LinkExtractor(allow=r'browse'), follow=True),
        Rule(LinkExtractor(allow=r'question/(\d+).html'), callback='parse_item', follow=True),
    )

    # def __init__(self, *args, **kwargs):
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(SicklistSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        print('response.url===========', response.url)
        item = SickItem()
        # 问题类目
        catOne = response.xpath('//div[@class="sub"]/span[2]/a/text()').extract()[0]
        catTwo = response.xpath('//div[@class="sub"]/span[3]/a/text()').extract()[0]
        catThree = response.xpath('//div[@class="sub"]/span[4]/a/text()').extract()
        catFour = response.xpath('//span[@class="sub_here"]/text()').extract()[0].strip()
        # 问题标题
        title = response.xpath('//p[@class="ask_tit"]/text()').extract()[0].strip()
        # 患者性别
        gender = response.xpath('//p[@class="mation"]/span[1]/text()').extract()[0]
        # 年龄
        age = response.xpath('//p[@class="mation"]/span[2]/text()').extract()
        # 发病时间
        startTime = response.xpath('//p[@class="mation"]/span[3]/text()').extract()
        # 问题描述
        question = response.xpath('//p[@class="txt_ms"]/text()').extract()[0].strip()
        # 提问时间
        questionTime = response.xpath('//p[@class="txt_nametime"]/span[2]/text()').extract()[0]
        # 问题标签
        questionTag = response.xpath('//p[@class="txt_label"]/span[not(@style)]/a/text()').extract()
        # 问题链接
        questionUrl = response.url

        strTag = ""
        for tag in questionTag:
            strTag += "|" + tag

        if response.xpath('//div[@class="sub"]/span[2]/a/text()[.!=""]'):
            item['catOne'] = catOne
        else:
            item['catOne'] = ""
        if response.xpath('//div[@class="sub"]/span[3]/a/text()'):
            item['catTwo'] = catTwo
        else:
            item['catTwo'] = ""
        if response.xpath('//div[@class="sub"]/span[4]/a/text()[.!=""]'):
            item['catThree'] = catThree[0]
        else:
            item['catThree'] = ""
        if response.xpath('//span[@class="sub_here"]/text()[.!=""]'):
            item['catFour'] = catFour.strip()
        else:
            item['catFour'] = ""
        item['title'] = title
        item['gender'] = gender
        if response.xpath('//p[@class="mation"]/span[2]/text()[.!=""]'):
            item['age'] = age[0].strip()
        else:
            item['age'] = ""
        if response.xpath('//p[@class="mation"]/span[3]/text()[.!=""]'):
            item['startTime'] = startTime[0]
        else:
            item['startTime'] = ""
        item['question'] = question
        item['questionTime'] = questionTime
        item['questionTag'] = strTag
        item['questionUrl'] = questionUrl
        yield item
