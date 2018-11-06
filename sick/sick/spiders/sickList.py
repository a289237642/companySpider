# -*- coding: utf-8 -*-

from sick.items import SickItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider


class SicklistSpider(RedisCrawlSpider):
    name = 'sickList'
    allowed_domains = ['ask.39.net']
    # start_urls = ['http://ask.39.net']

    # scrapy-redis
    redis_key = 'myspider:start_urls'
    # 规则爬虫
    rules = (
        Rule(LinkExtractor(allow=r'question/(\d+).html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print('response.url===========', response.url)
        item = SickItem()
        # 问题类目一
        if len(response.xpath('//div[@class="sub"]/span[2]/a/text()')) > 0:
            catOne = response.xpath('//div[@class="sub"]/span[2]/a/text()').extract()[0]
        else:
            catOne = ""
        # 问题类目二
        if len(response.xpath('//div[@class="sub"]/span[3]/a/text()')) > 0:
            catTwo = response.xpath('//div[@class="sub"]/span[3]/a/text()').extract()[0]
        else:
            catTwo = ""
        # 问题类目三
        if len(response.xpath('//div[@class="sub"]/span[4]/a/text()')) > 0:
            catThree = response.xpath('//div[@class="sub"]/span[4]/a/text()').extract()[0]
        else:
            catThree = ""
        # 问题类目四
        if len(response.xpath('//span[@class="sub_here"]/text()')) > 0:
            catFour = response.xpath('//span[@class="sub_here"]/text()').extract()[0].strip()
        else:
            catFour = ''

        # 问题标题
        if len(response.xpath('//p[@class="ask_tit"]/text()')) > 0:
            title = response.xpath('//p[@class="ask_tit"]/text()').extract()[0].strip()
        else:
            title = ''
        # 患者性别
        if len(response.xpath('//p[@class="mation"]/span[1]/text()')) > 0:
            gender = response.xpath('//p[@class="mation"]/span[1]/text()').extract()[0]
        else:
            gender = ''
        # 年龄
        if len(response.xpath('//p[@class="mation"]/span[2]/text()')) > 0:
            age = response.xpath('//p[@class="mation"]/span[2]/text()').extract()[0]
        else:
            age = ""
        # 发病时间
        if len(response.xpath('//p[@class="mation"]/span[3]/text()')) > 0:
            startTime = response.xpath('//p[@class="mation"]/span[3]/text()').extract()[0]
        else:
            startTime = ""
        # 问题描述
        if len(response.xpath('//p[@class="txt_ms"]/text()')) > 0:
            question = response.xpath('//p[@class="txt_ms"]/text()').extract()[0].strip()
        else:
            question = ""
        # 提问时间
        if len(response.xpath('//p[@class="txt_nametime"]/span[2]/text()')) > 0:
            questionTime = response.xpath('//p[@class="txt_nametime"]/span[2]/text()').extract()[0]
        else:
            questionTime = ""
        # 问题标签
        if len(response.xpath('//p[@class="txt_label"]/span[not(@style)]/a/text()')) > 0:
            questionTag = response.xpath('//p[@class="txt_label"]/span[not(@style)]/a/text()').extract()
        else:
            questionTag = ""
        # 问题链接
        questionUrl = response.url

        strTag = ""
        for tag in questionTag:
            strTag += "|" + tag

        item['catOne'] = catOne
        item['catTwo'] = catTwo
        item['catThree'] = catThree
        item['catFour'] = catFour.strip()
        item['title'] = title
        item['gender'] = gender
        item['age'] = age.strip()
        item['startTime'] = startTime
        item['question'] = question
        item['questionTime'] = questionTime
        item['questionTag'] = strTag
        item['questionUrl'] = questionUrl
        yield item
