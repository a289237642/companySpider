# -*- coding: utf-8 -*-
import scrapy


class BaikeSpider(scrapy.Spider):
    name = 'baike'
    allowed_domains = ['baike.baidu.com']

    start_urls = ['https://baike.baidu.com/item/Python/407313']

    def parse(self, response):
        content = response.xpath('//div[@class="main-content"]')
        print('-' * 40)
        print(content)
        titles = content.xpath('//div[@class="para-title level-2"]')
        print(len(titles))
        print(titles)

        # aa = content.xpath('//div[preceding::div[@class="para-title level-2"][1] and following::div[@class="para-title level-2"][2]]')

        aa = content.xpath('//*[count(preceding-sibling::div[@class="para-title level-2"])=1]')

        print(aa)
        print(aa.extract())
        print(len(aa))

        # for k, v in enumerate(titles):
        #     if k == 0:
        #         v.xpath('//div[@class="para-title level-2"]')

        # print(content.extract_first())
        return {}
