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

    # 处理路径
    def handlerpath(self, url):

        st1 = url.split('/')[-1]
        st2 = url.split('/')[-2]
        st3 = url.split('/')[-3]
        st4 = ""
        st4 += st3 + "/" + st2 + "/" + st1
        return st4

    # 处理js动态加载
    def handlejs(self, url):

        driver = webdriver.Chrome()
        driver.get(url)

        CYRS = driver.find_element_by_xpath('//em[@class="js_joinNum"][1]').text
        PLS = driver.find_element_by_xpath('//em[@class="js_cmtNum"][1]').text
        TJS = driver.find_element_by_xpath('//div[@id="left_dz"]/span').text
        urlpath = self.handlerpath(url)
        filename = os.path.join(PREFIX, WEBSITE, urlpath.strip('/'))
        file_dir = os.path.dirname(filename)
        os.makedirs(file_dir, exist_ok=True)
        with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(driver.page_source)

        driver.close()
        return CYRS, PLS, TJS, filename

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
                    '//div[@class="theLogo"]/div/a[2]/text()|//div[@class="h_nav"]/a[2]/text()')) == 0:
                LMLJ2 = ""
            else:
                LMLJ2 = \
                    response.xpath(
                        '//div[@class="theLogo"]/div/a[2]/text()|//div[@class="h_nav"]/a[2]/text()').extract()[
                        0]
                if LMLJ2 == "台湾" or LMLJ2 == "大陆" or LMLJ2 == "国际" or LMLJ2 == "港澳":
                    # 标题
                    BTIT = response.xpath(
                        '//div[@id="titL"]/h1/text()|//div[@class="yc_tit"]/h1/text()|//h1[@id="artical_topic"]/text()').extract()[
                        0]
                    # 参与人数，评论数，推荐数,路径
                    CYRS, PLS, TJS, filename = self.handlejs(response.url)
                    # 新闻来源
                    XWLY = response.xpath(
                        '//span[@class="ss03"]/text()|//div[@id="yc_con_txt"]/p/text()|//span[@class="ss03"]/a/text()|//span[@class="ss03 weMediaicon"]/a/text()').extract()[
                        0]
                    # 编者
                    if len(response.xpath(
                            '//div[@id="artical_sth2"]/p[1]/text()|//div[@id="main_content"]/p[12]/text()|//span[@class="ss04"]/span/text()')) == 0:
                        BZ = ""
                    else:
                        BZ = response.xpath(
                            '//div[@id="artical_sth2"]/p[1]/text()|//div[@id="main_content"]/p[12]/text()|//span[@class="ss04"]/span/text()').extract()[
                            0]
                    # 栏目路径
                    LMLJ1 = \
                        response.xpath(
                            '//div[@class="speNav js_crumb"]/a[1]/text()|//div[@class="h_nav"]/a[1]/text()|//div[@class="theLogo"]/div/a[1]/text()').extract()[
                            0]

                    if len(response.xpath('//span[@class="ss01"]/text()')) == 0:
                        CGSJ = ""
                    else:
                        CGSJ = response.xpath('//span[@class="ss01"]/text()').extract()[0]
                    LMLJ = ""
                    LMLJ += LMLJ1 + ";" + LMLJ2
                    # 正文文本
                    ZWWB = response.xpath('//div[@id="main_content"]/p/text()').extract()[0]
                    # 正文内容
                    ZWNR = ZWWB
                    # 新闻缩略图的url
                    TP_URL = response.xpath(
                        '//p[@class="detailPic"]/img/@src|//div[@class="yc_con_txt"]/p/img/@src|//div[@id="main_content"]/p/img/@src|//div[@class="box02"][1]/img/@src').extract()[
                        0]
                    item['BTIT'] = BTIT
                    item['CYRS'] = CYRS
                    item['PLS'] = PLS
                    item['XWLY'] = XWLY
                    item['LMLJ'] = LMLJ
                    item['ZWWB'] = ZWWB
                    item['BZ'] = BZ
                    item['TJS'] = TJS
                    item['CJSJ'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    item['ZWNR'] = ZWNR
                    item['TP_URL'] = TP_URL
                    item['YS_URL'] = filename
                    item['CL_URL'] = filename
                    item['CGSJ'] = CGSJ
                    # print(item)
                    yield item
