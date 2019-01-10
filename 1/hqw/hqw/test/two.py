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
from selenium.webdriver.chrome.options import Options

from hqw.config import windows_chrome_driver, linux_chrome_driver, get_chrome_options


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
            chrome_options = get_chrome_options()
            driver = webdriver.Chrome(executable_path=windows_chrome_driver, chrome_options=chrome_options)
            driver.get(response.url)
            htmls = etree.HTML(driver.page_source)

            item = HqwItem()

            # 一级类目
            if len(htmls.xpath(
                    '//div[@class="topPath"]/a[1]/text()|//div[@class="nav_left"]/a[1]/text()|//div[@class="a_path"]/ul/li[1]/a/text()')) == 0:
                catOne = ""
            else:
                catOne = \
                    htmls.xpath(
                        '//div[@class="topPath"]/a[1]/text()|//div[@class="nav_left"]/a[1]/text()|//div[@class="a_path"]/ul/li[1]/a/text()')[
                        0]

            # 二级类目
            if len(htmls.xpath(
                    '//div[@class="topPath"]/a[2]/text()|//div[@class="nav_left"]/a[2]/text()|//div[@class="a_path"]/ul/li[2]/a/text()')) == 0:
                catTwo = ""
            else:
                catTwo = \
                    htmls.xpath(
                        '//div[@class="topPath"]/a[2]/text()|//div[@class="nav_left"]/a[2]/text()|//div[@class="a_path"]/ul/li[2]/a/text()')[
                        0]
            # 三级类目
            if len(htmls.xpath(
                    '//div[@class="topPath"]/a[3]/text()|//div[@class="nav_left"]/a[3]/text()|//div[@class="a_path"]/ul/li[3]/a/text()')) == 0:
                catThree = ""
            else:
                catThree = \
                    htmls.xpath(
                        '//div[@class="topPath"]/a[3]/text()|//div[@class="nav_left"]/a[3]/text()|//div[@class="a_path"]/ul/li[3]/a/text()')[
                        0]

            # 栏目路径
            LMLJ = ""
            LMLJ += catOne + ";" + catTwo + ";" + catThree
            # 新闻标题
            if len(htmls.xpath(
                    '//h1[@class="tle"]/text()|//div[@class="conText"]/h1/text()|//h1[@class="hd"]/strong/text()')) == 0:
                BTIT = ""
            else:
                BTIT = htmls.xpath(
                    '//h1[@class="tle"]/text()|//div[@class="conText"]/h1/text()|//h1[@class="hd"]/strong/text()')[0]

            # 成稿时间
            if len(htmls.xpath(
                    '//span[@class="la_t_a"]/text()|//strong[@id="pubtime_baidu"]/text()|//div[@class="summary"]/strong[1]/text()|//li[@class="time"]/div/span/text()')) == 0:
                CGSJ = ""
            else:
                CGSJ = htmls.xpath(
                    '//span[@class="la_t_a"]/text()|//strong[@id="pubtime_baidu"]/text()|//div[@class="summary"]/strong[1]/text()|//li[@class="time"]/div/span/text()')[
                    0]

            # 新闻来源
            if len(htmls.xpath(
                    '//span[@class="la_t_b"]/a/text()|//strong[@id="source_baidu"]/a/text()|//ul[@class="tool_l"]/li[2]/span/a/text()')) == 0:
                XWLY = ""
            else:
                XWLY = \
                    htmls.xpath(
                        '//span[@class="la_t_b"]/a/text()|//strong[@id="source_baidu"]/a/text()|//ul[@class="tool_l"]/li[2]/span/a/text()')[
                        0]
            # 编者
            if len(htmls.xpath(
                    '//span[@class="author"]/text()|//div[@id="editor_baidu"]/span/text()|//li[@class="user"]/div/span/text()|//div[@class="la_edit"]/span/text()')) == 0:
                BZ = ""
            else:
                BZ = htmls.xpath(
                    '//span[@class="author"]/text()|//div[@id="editor_baidu"]/span/text()|//li[@class="user"]/div/span/text()|//div[@class="la_edit"]/span/text()')[
                    0]
            # 参与人数
            if len(htmls.xpath(
                    '//span[@id="msgNumBottom"]/a/text()|//b[@id="msgNumTop"]/a/text()|//b[@id="msgNumBottom"]/a/text()|//span[@class="participate"]/var[0]/text()')) == 0:
                CYRS = ""
            else:
                CYRS = htmls.xpath(
                    '//span[@id="msgNumBottom"]/a/text()|//b[@id="msgNumTop"]/a/text()|//b[@id="msgNumBottom"]/a/text()|//span[@class="participate"]/var[0]/text()')[
                    0]

            # 正文文本
            if len(htmls.xpath('//div[@class="la_con"]/p/text()|//div[@class="text"]/p/text()')) == 0:
                ZWWB = ""
            else:
                ZWWB = htmls.xpath('//div[@class="la_con"]/p/text()|//div[@class="text"]/p/text()')
                ZWWB = ''.join(ZWWB)
            # 图片的url
            if len(htmls.xpath(
                    '//div[@class="la_con"]/p[2]/img/@src|//div[@id="text"]/p/img/@src|//div[@class="la_con"]/p/img/@src|//div[@id="picWrap"]/img/@src')) == 0:
                TP_URL = ""
            else:
                TP_URL = htmls.xpath(
                    '//div[@class="la_con"]/p[2]/img/@src|//div[@id="text"]/p/img/@src|//div[@class="la_con"]/p/img/@src|//div[@id="picWrap"]/img/@src')[
                    0]

            urlpath = response.url  # 这是那个  ---http://news.ifeng.com/a/20190108/60227925_0.shtml
            WEBSITE = r'huanqiu/' + catTwo + '/html/'
            filename = os.path.join(WEBSITE, urlpath.split('/')[-1].strip('/'))
            file_dir = os.path.dirname(filename)
            os.makedirs(file_dir, exist_ok=True)
            with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(driver.page_source)

            item['BTIT'] = BTIT
            item['XWLY'] = XWLY
            item['LMLJ'] = LMLJ
            item['ZWWB'] = ZWWB.replace("\u3000\u3000", "")
            item['ZWNR'] = ZWWB

            item['TP_URL'] = TP_URL
            item['BZ'] = BZ
            item['CJSJ'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['CGSJ'] = CGSJ
            item['CYRS'] = CYRS
            # # 原始网页链接
            item['YS_URL'] = filename
            # # 处理网页链接
            item['CL_URL'] = filename
            item['URL'] = response.url
            item['catTwo'] = catTwo

            driver.close()
            print(item)
            yield item
