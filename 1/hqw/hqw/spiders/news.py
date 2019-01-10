# -*- coding: utf-8 -*-
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from hqw.items import HqwItem
from datetime import datetime
from selenium import webdriver

from hqw.config import windows_chrome_driver, linux_chrome_driver, get_chrome_options


class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['tech.huanqiu.com']
    start_urls = ['http://tech.huanqiu.com/']
    # start_urls = ['http://oversea.huanqiu.com/', 'http://world.huanqiu.com/', 'http://china.huanqiu.com/',
    #               'http://taiwan.huanqiu.com/']
    # start_urls = ['http://mil.huanqiu.com/', 'http://tech.huanqiu.com/', 'http://world.huanqiu.com/',
    #               'http://oversea.huanqiu.com/', 'http://taiwan.huanqiu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'diginews/(\d+)-(\d+)/(\d+).html'), callback='parse_item', follow=True),
    )

    def handlejs(self, url):
        chrome_options = get_chrome_options()
        driver = webdriver.Chrome(executable_path=linux_chrome_driver, chrome_options=chrome_options)
        driver.get(url)
        # 参与人数
        CYRS = driver.find_element_by_xpath(
            '//span[@id="msgNumBottom"]/a|//b[@id="msgNumTop"]/a|//b[@id="msgNumBottom"]/a|//span[@class="participate"]/var[0]').text
        return CYRS

    # 判断时间
    def handlertime(self, url):
        list1 = url.split("/")[-2].split("-")
        listtime = list1[0] + list1[1]
        return listtime

    def parse_item(self, response):
        print("=======", response.url)

        atime = self.handlertime(response.url)
        if int(atime) >= 201806:

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
            CYRS = self.handlejs(response.url)

            # 正文文本
            if len(response.xpath('//div[@class="la_con"]/p/text()|//div[@class="text"]/p/text()')) == 0:
                ZWWB = ""
            else:
                ZWWB = response.xpath('//div[@class="la_con"]/p/text()|//div[@class="text"]/p/text()').extract()
                ZWWB = ''.join(ZWWB)
            # 图片的url
            if len(response.xpath(
                    '//div[@class="la_con"]/p[2]/img/@src|//div[@id="text"]/p/img/@src|//div[@class="la_con"]/p/img/@src|//div[@id="picWrap"]/img/@src')) == 0:
                TP_URL = ""
            else:
                TP_URL = response.xpath(
                    '//div[@class="la_con"]/p[2]/img/@src|//div[@id="text"]/p/img/@src|//div[@class="la_con"]/p/img/@src|//div[@id="picWrap"]/img/@src').extract()[
                    0]

            urlpath = response.url  # 这是那个  ---http://news.ifeng.com/a/20190108/60227925_0.shtml
            WEBSITE = r'huanqiu/' + catTwo + '/html/'
            filename = os.path.join(WEBSITE, urlpath.split('/')[-1].strip('/'))
            file_dir = os.path.dirname(filename)
            os.makedirs(file_dir, exist_ok=True)
            with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(response.text)

            item['BTIT'] = BTIT
            item['XWLY'] = XWLY
            item['LMLJ'] = LMLJ
            item['ZWWB'] = ZWWB.replace("\n", "").replace("\u3000\u3000", "")
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

            # print(item)
            yield item

# if __name__ == '__main__':
#     print(windows_chrome_driver)
