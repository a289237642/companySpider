# -*- coding: utf-8 -*-
import os
import scrapy
import base64
import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from hqw.items import HqwItem
from datetime import datetime
from lxml import etree
from selenium import webdriver


class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['huanqiu.com']
    start_urls = ['http://mil.huanqiu.com/', 'http://tech.huanqiu.com/', 'http://world.huanqiu.com/',
                  'http://oversea.huanqiu.com/', 'http://taiwan.huanqiu.com/', 'http://www.huanqiu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'(\w+)/(\d+)-(\d+)/(\d+).html'), callback='parse_item', follow=True),
    )

    def process_image_src(self, source, img_xpath):
        print('process: ', type(source))
        html = etree.HTML(source)
        images = html.xpath(img_xpath)

        if images:
            img = images[0]
            img_url = img.get('src')
            img_b64 = self.image_base64(img_url)
            if img_b64:
                src = 'data:image/jpg;base64,{b64}'.format(b64=img_b64)
                img.set('src', src)
                return etree.tostring(html).decode('utf-8')
            else:
                return source
        else:
            return source

    def image_base64(self, url):
        try:
            r = requests.get(url, timeout=20)
            return base64.b64encode(r.content).decode('utf-8')
        except Exception as e:
            return ''

    # 判断时间
    def handlertime(self, url):
        list1 = url.split("/")[-2].split("-")
        listtime = list1[0] + list1[1]
        return listtime

    def parse_item(self, response):
        print("=======", response.url)
        atime = self.handlertime(response.url)
        if int(atime) >= 201806:

            driver = webdriver.Chrome()
            driver.get(response.url)
            htmls=etree.HTML(driver.page_source)
            item = HqwItem()
            # 一级类目
            if len(response.xpath(
                    '//div[@class="topPath"]/a[1]/text()|//div[@class="nav_left"]/a[1]/text()|//div[@class="a_path"]/ul/li[1]/a/text()')) == 0:
                catOne = ""
            else:
                catOne = \
                    response.xpath(
                        '//div[@class="topPath"]/a[1]/text()|//div[@class="nav_left"]/a[1]/text()|//div[@class="a_path"]/ul/li[1]/a/text()').extract()[
                        0]
            # 二级类目
            if len(response.xpath(
                    '//div[@class="topPath"]/a[2]/text()|//div[@class="nav_left"]/a[2]/text()|//div[@class="a_path"]/ul/li[2]/a/text()')) == 0:
                catTwo = ""
            else:
                catTwo = \
                    response.xpath(
                        '//div[@class="topPath"]/a[2]/text()|//div[@class="nav_left"]/a[2]/text()|//div[@class="a_path"]/ul/li[2]/a/text()').extract()[
                        0]
            # 三级类目
            if len(response.xpath(
                    '//div[@class="topPath"]/a[3]/text()|//div[@class="nav_left"]/a[3]/text()|//div[@class="a_path"]/ul/li[3]/a/text()')) == 0:
                catThree = ""
            else:
                catThree = \
                    response.xpath(
                        '//div[@class="topPath"]/a[3]/text()|//div[@class="nav_left"]/a[3]/text()|//div[@class="a_path"]/ul/li[3]/a/text()').extract()[
                        0]
            # 栏目路径
            LMLJ = ""
            LMLJ += catOne + ";" + catTwo + ";" + catThree
            # 新闻标题
            if len(response.xpath(
                    '//h1[@class="tle"]/text()|//div[@class="conText"]/h1/text()|//h1[@class="hd"]/strong/text()')) == 0:
                BTIT = ""
            else:
                BTIT = response.xpath(
                    '//h1[@class="tle"]/text()|//div[@class="conText"]/h1/text()|//h1[@class="hd"]/strong/text()').extract()[
                    0]
            # 成稿时间
            if len(response.xpath(
                    '//span[@class="la_t_a"]/text()|//strong[@id="pubtime_baidu"]/text()|//div[@class="summary"]/strong[1]/text()|//li[@class="time"]/div/span/text()')) == 0:
                CGSJ = ""
            else:
                CGSJ = response.xpath(
                    '//span[@class="la_t_a"]/text()|//strong[@id="pubtime_baidu"]/text()|//div[@class="summary"]/strong[1]/text()|//li[@class="time"]/div/span/text()').extract()[
                    0]
            # 新闻来源
            if len(response.xpath(
                    '//span[@class="la_t_b"]/a/text()|//strong[@id="source_baidu"]/a/text()|//ul[@class="tool_l"]/li[2]/span/a/text()')) == 0:
                XWLY = ""
            else:
                XWLY = \
                    response.xpath(
                        '//span[@class="la_t_b"]/a/text()|//strong[@id="source_baidu"]/a/text()|//ul[@class="tool_l"]/li[2]/span/a/text()').extract()[
                        0]
            # 编者
            if len(response.xpath(
                    '//span[@class="author"]/text()|//div[@id="editor_baidu"]/span/text()|//li[@class="user"]/div/span/text()|//div[@class="la_edit"]/span/text()')) == 0:
                BZ = ""
            else:
                BZ = response.xpath(
                    '//span[@class="author"]/text()|//div[@id="editor_baidu"]/span/text()|//li[@class="user"]/div/span/text()|//div[@class="la_edit"]/span/text()').extract()[
                    0]
            # 参与人数
            if len(response.xpath(
                    '//span[@id="msgNumBottom"]/a/text()|//b[@id="msgNumTop"]/a/text()|//b[@id="msgNumBottom"]/a/text()|//span[@class="participate"]/var[0]/text()')) == 0:
                CYRS = ""
            else:
                CYRS = response.xpath(
                    '//span[@id="msgNumBottom"]/a/text()|//b[@id="msgNumTop"]/a/text()|//b[@id="msgNumBottom"]/a/text()|//span[@class="participate"]/var[0]/text()').extract()[
                    0]
            # 正文文本
            if len(response.xpath('//div[@class="la_con"]/p/text()|//div[@class="text"]/p/text()')) == 0:
                ZWWB = ""
            else:
                ZWWB = response.xpath('//div[@class="la_con"]/p/text()|//div[@class="text"]/p/text()').extract()
            # 图片的url
            if len(response.xpath(
                    '//div[@class="la_con"]/p[2]/img/@src|//div[@id="text"]/p/img/@src|//div[@class="la_con"]/p/img/@src|//div[@id="picWrap"]/img/@src')) == 0:
                TP_URL = ""
            else:
                TP_URL = response.xpath(
                    '//div[@class="la_con"]/p[2]/img/@src|//div[@id="text"]/p/img/@src|//div[@class="la_con"]/p/img/@src|//div[@id="picWrap"]/img/@src').extract()[
                    0]

            item['BTIT'] = BTIT
            item['XWLY'] = XWLY
            item['LMLJ'] = LMLJ
            item['ZWWB'] = ZWWB

            item['TP_URL'] = TP_URL
            item['BZ'] = BZ
            item['CJSJ'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['CGSJ'] = CGSJ
            item['CYRS'] = CYRS
            item['URL'] = response.url
            # print(item)
            yield item
