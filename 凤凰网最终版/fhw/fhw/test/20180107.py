# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fhw.items import FhwItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

WEBSITE = r'ifeng'


class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/hongkong/']

    rules = (
        Rule(LinkExtractor(allow=r'a/(\d+)/(\d+)_(\d+).shtml'), callback='parse_item', follow=True),
    )

    # 处理js动态加载
    def handlejs(self, response):
        item = FhwItem()
        chrome_options = Options()
        # 设置chrome浏览器无界面模式
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver.manage().timeouts().setScriptTimeout(3, TimeUnit.SECONDS);

        # driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        driver.get(response.url)
        LMLJ2 = driver.find_element_by_xpath('//div[@class="theLogo"]/div/a[2]|//div[@class="h_nav"]/a[2]').text
        if len(driver.find_element_by_xpath(
                '//div[@class="theLogo"]/div/a[2]|//div[@class="h_nav"]/a[2]').text) > 0 and LMLJ2 == "台湾" or LMLJ2 == "大陆" or LMLJ2 == "国际" or LMLJ2 == "港澳":
            CYRS = driver.find_element_by_xpath('//em[@class="js_joinNum"][1]').text
            PLS = driver.find_element_by_xpath('//em[@class="js_cmtNum"][1]').text
            TJS = driver.find_element_by_xpath('//div[@id="left_dz"]/span').text
            BT = driver.find_element_by_xpath(
                '//div[@id="titL"]/h1|//div[@class="yc_tit"]/h1|//h1[@id="artical_topic"]').text
            XWLY = driver.find_element_by_xpath(
                '//div[@id="yc_con_txt"]/p|//span[@class="ss03"]/a|//span[@class="ss03 weMediaicon"]/a').text
            BZ = driver.find_element_by_xpath(
                '//div[@id="artical_sth2"]/p[1]').text
            LMLJ1 = driver.find_element_by_xpath(
                '//div[@class="speNav js_crumb"]/a[1]|//div[@class="h_nav"]/a[1]|//div[@class="theLogo"]/div/a[1]').text
            LMLJ = ""
            LMLJ += LMLJ1 + ";" + LMLJ2
            CGSJ = driver.find_element_by_xpath('//span[@class="ss01"]').text
            ss = driver.find_element_by_xpath(
                '//p[@class="detailPic"]/img|//div[@class="yc_con_txt"]/p/img|//div[@id="main_content"]/p/img|//div[@class="box02"][1]/img')
            ZWWB = driver.find_element_by_xpath('//div[@id="main_content"]').text
            TP_URL = ss.get_attribute('src')
            # ZWNR = ZWWB + "|" + TP_URL
            urlpath = response.url  # 这是那个  ---http://news.ifeng.com/a/20190108/60227925_0.shtml
            WEBSITE = r'ifeng/' + LMLJ2 + '/html/'
            filename = os.path.join(WEBSITE, urlpath.split('/')[-1].strip('/'))
            file_dir = os.path.dirname(filename)
            os.makedirs(file_dir, exist_ok=True)
            with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(driver.page_source)

            item['BTIT'] = BT
            item['CYRS'] = CYRS
            item['PLS'] = PLS
            item['XWLY'] = XWLY
            item['LMLJ'] = LMLJ
            item['ZWWB'] = ZWWB
            item['BZ'] = BZ
            item['CGSJ'] = CGSJ
            item['TJS'] = TJS
            item['CJSJ'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['ZWNR'] = ZWWB
            item['TP_URL'] = TP_URL
            item['YS_URL'] = filename
            item['CL_URL'] = filename
            item['LMLJ2'] = LMLJ2

            driver.close()
            yield item

    def parse_item(self, response):
        print("====", response.url)
        aitem = response.url
        # 判断新闻在20180601之后的新闻
        if int(aitem.split("/")[4]) >= 20180601:
            yield scrapy.Request(response.url, callback=self.handlejs, dont_filter=True)
