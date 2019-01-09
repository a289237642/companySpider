# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fhw.items import FhwItem
from selenium import webdriver
from datetime import datetime

PREFIX = r'Z:\\'
WEBSITE = r'ifeng'


class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/hongkong/']

    rules = (
        Rule(LinkExtractor(allow=r'a/(\d+)/(\d+)_(\d+).shtml'), callback='parse_item', follow=True),
    )

    # 处理js动态加载
    def handlejs(self, url):
        o = urlparse(url)

        driver = webdriver.Chrome()
        driver.get(url)

        CYRS = driver.find_element_by_xpath('//em[@class="js_joinNum"][1]').text
        PLS = driver.find_element_by_xpath('//em[@class="js_cmtNum"][1]').text
        TJS = driver.find_element_by_xpath('//div[@id="left_dz"]/span').text

        filename = os.path.join(PREFIX, WEBSITE, o.path.strip('/'))
        file_dir = os.path.dirname(filename)
        os.makedirs(file_dir, exist_ok=True)
        with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(driver.page_source)

        driver.close()
        return CYRS, PLS, TJS

    # 判断新闻在20180601之后的新闻
    def strUrl(self, str):
        str1 = str.split("/")[4]
        return str1

    def parse_item(self, response):
        print("====", response.url)
        item = FhwItem()
        atime = self.strUrl(response.url)
        if int(atime) >= 20180601:
            if len(response.xpath(
                    'div[@class="speNav js_crumb"]/a[2]/text()|//div[@class="h_nav"]/a[1]/text()|//div[@class="theLogo"]/div/a[1]/text()|//div[@class="speNav js_crumb"]/a[2]/text()')) > 0:
                LMLJ2 = \
                    response.xpath(
                        'div[@class="speNav js_crumb"]/a[2]/text()|//div[@class="h_nav"]/a[1]/text()|//div[@class="theLogo"]/div/a[1]/text()|//div[@class="speNav js_crumb"]/a[2]/text()').extract()[
                        0]
                if LMLJ2 == "台湾" or LMLJ2 == "大陆" or LMLJ2 == "国际" or LMLJ2 == "港澳":
                    # 标题
                    if len(response.xpath(
                            '//div[@id="titL"]/h1/text()|//div[@class="yc_tit"]/h1/text()|//h1[@id="artical_topic"]/text()')) > 0:
                        BTIT = response.xpath(
                            '//div[@id="titL"]/h1/text()|//div[@class="yc_tit"]/h1/text()|//h1[@id="artical_topic"]/text()').extract()[
                            0]
                    else:
                        BTIT = ""
                    CYRS, PLS, TJS = self.handlejs(response.url)
                    if len(response.xpath(
                            '//span[@class="ss03"]/text()|//div[@id="yc_con_txt"]/p/text()|//span[@class="ss03"]/a/text()|//span[@class="ss03 weMediaicon"]/a/text()')) > 0:
                        XWLY = response.xpath(
                            '//span[@class="ss03"]/text()|//div[@id="yc_con_txt"]/p/text()|//span[@class="ss03"]/a/text()|//span[@class="ss03 weMediaicon"]/a/text()').extract()[
                            0]
                    else:
                        XWLY = ""
                    if len(response.xpath(
                            '//div[@id="artical_sth2"]/p[1]/text()|//div[@id="main_content"]/p[12]/text()|//span[@class="ss04"]/span/text()')) == 0:
                        BZ = ""
                    else:
                        BZ = response.xpath(
                            '//div[@id="artical_sth2"]/p[1]/text()|//div[@id="main_content"]/p[12]/text()|//span[@class="ss04"]/span/text()').extract()[
                            0]
                    # 栏目路径
                    if len(response.xpath(
                            '//div[@class="speNav js_crumb"]/a[1]/text()|//div[@class="h_nav"]/a[1]/text()|//div[@class="theLogo"]/div/a[1]/text()')) > 0:
                        LMLJ1 = \
                            response.xpath(
                                '//div[@class="speNav js_crumb"]/a[1]/text()|//div[@class="h_nav"]/a[1]/text()|//div[@class="theLogo"]/div/a[1]/text()').extract()[
                                0]
                    else:
                        LMLJ1 = ""
                    # if len(response.xpath(
                    #         '//div[@class="speNav js_crumb"]/a[2]/text()|//div[@class="h_nav"]/a[1]/text()|//div[@class="theLogo"]/div/a[1]/text()')) > 0:
                    #     LMLJ2 = \
                    #         response.xpath(
                    #             '//div[@class="theLogo"]/div/a[2]/text()|//div[@class="h_nav"]/a[2]/text()').extract()[
                    #             0]
                    LMLJ = ""
                    LMLJ += LMLJ1 + ";" + LMLJ2
                    ZWWB = response.xpath('//div[@id="main_content"]/p/text()').extract()[0]
                    ZWNR = ZWWB
                    if len(response.xpath(
                            '//p[@class="detailPic"]/img/@src|//div[@class="yc_con_txt"]/p/img/@src|//div[@id="main_content"]/p/img/@src|//div[@class="box02"][1]/img/@src')) > 0:
                        TP_URL = response.xpath(
                            '//p[@class="detailPic"]/img/@src|//div[@class="yc_con_txt"]/p/img/@src|//div[@id="main_content"]/p/img/@src|//div[@class="box02"][1]/img/@src').extract()[
                            0]
                    else:
                        TP_URL = ""

                    item['BTIT'] = BTIT
                    item['CYRS'] = int(CYRS)
                    item['PLS'] = int(PLS)
                    item['XWLY'] = XWLY
                    item['LMLJ'] = LMLJ
                    item['ZWWB'] = ZWWB
                    item['BZ'] = BZ
                    item['TJS'] = TJS
                    item['CJSJ'] = datetime.now()
                    item['ZWNR'] = ZWNR
                    item['TP_URL'] = TP_URL
                    item['YS_URL'] = response.url
                    item['CL_URL'] = response.url
                    print(item)
                    yield item
