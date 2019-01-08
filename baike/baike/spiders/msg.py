# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from baike.items import BaikeItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime


class MsgSpider(CrawlSpider):
    name = 'msg'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com']

    rules = (
        Rule(LinkExtractor(allow=r'item/(\w+)'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print("==========>>>>", response.url)
        item = BaikeItem()
        # ------------------------主表的信息-------------------------------------

        # 百科记录标识
        BKID = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()[0]

        if len(response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dd[2]/text()')) > 0:
            fname = response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dd[2]/text()').extract()
            # 百科英文名称
            YWMC = fname[0]
            # 百科其他名称
            QTMC = str(fname)
        else:
            YWMC = ""
            QTMC = ""
        # 百科解释
        BKJS = response.xpath('//div[@class="lemma-summary"]').xpath('string(.)').extract_first()

        # 分类路径
        FLLJ = str(response.xpath('//span[@class="taglist"]/text()').extract())
        # 图片缩略图链接
        if len(response.xpath('//div[@class="summary-pic"]/a/img/@src').extract()) > 0:
            TP_URL = response.xpath('//div[@class="summary-pic"]/a/img/@src').extract()
        else:
            TP_URL = ""
        # print("==FLLJ===", FLLJ, type(FLLJ))

        # ------------------------主表的信息-------------------------------------

        # ------------------------从表的信息-------------------------------------
        # 属性名称
        SXMC = response.xpath('//h2[@class="title-text"]/text()').extract()
        # 属性类型
        # SXLX
        # 属性值
        SXZ = response.xpath('//div[@class="para"]').xpath('string(.)').extract_first()
        # ------------------------从表的信息-------------------------------------

        item['BKID'] = BKID
        item['YWMC'] = YWMC
        item['QTMC'] = QTMC
        item['BKJS'] = BKJS
        item['FLLJ'] = FLLJ
        item['TP_URL'] = TP_URL
        item['SXMC'] = SXMC
        item['SXZ'] = SXZ
        item['CJSJ'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['URL'] = response.url
        print(item)
