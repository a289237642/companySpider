# -*- coding: utf-8 -*-
import os
import base64
import scrapy
import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fhw.items import FhwItem
from selenium import webdriver
from datetime import datetime
import re
from lxml import etree

from fhw.config import windows_chrome_driver, linux_chrome_driver, get_chrome_options


class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/listpage/11490/20181231/1/rtlist.shtml',
                  'http://news.ifeng.com/listpage/11528/0/1/rtlist.shtml',
                  'http://news.ifeng.com/listpage/11574/0/1/rtlist.shtml',
                  'http://news.ifeng.com/listpage/7609/0/1/rtlist.shtml']

    rules = (
        Rule(LinkExtractor(allow=r'rtlist.shtml$'), callback='parse_item', follow=True),
    )

    def process_image_src(self, source, img_xpath):
        # print('process: ', type(source))
        html = etree.HTML(source)
        images = html.xpath(img_xpath)

        if images:
            img = images[0]
            img_url = img.get('src')
            img_b64 = self.image_base64(img_url)
            if img_b64:
                src = 'data:image/jpg;base64,{b64}'.format(b64=img_b64)
                img.set('src', src)
                return etree.tostring(html, encoding='utf-8').decode('utf-8')
            else:
                return source
        else:
            return source

    def image_base64(self, url):
        try:
            r = requests.get(url, timeout=20)
            return base64.b64encode(r.content)
        except Exception as e:
            return ''

    def parse_datel(self, response):
        '''
        该方法用于处理详情页信息
        通过xpath定位出相应的数据
        '''
        print("====", response.url)
        chrome_options = get_chrome_options()
        driver = webdriver.Chrome(executable_path=windows_chrome_driver, chrome_options=chrome_options)
        driver.get(response.url)
        htmls = etree.HTML(driver.page_source)
        item = FhwItem()

        # 文章标题
        if len(htmls.xpath('//div[@class="yc_tit"]/h1/text()|//div[@id="artical"]/h1/text()')) > 0:
            title = htmls.xpath('//div[@class="yc_tit"]/h1/text()|//div[@id="artical"]/h1/text()')[0]
        else:
            title = ""
        # 正文文本
        if len(htmls.xpath('//div[@id="main_content"]/p/text()|//div[@id="main_content"]/text()')) > 0:
            cont = htmls.xpath('//div[@id="main_content"]/p/text()|//div[@id="main_content"]/text()')
            cont = ''.join(cont)
        else:
            cont = ""
        # 新闻来源
        if len(htmls.xpath('//span[@class="ss03"]/a/text()|//div[@class="yc_tit"]/p/a/text()')) > 0:
            source = htmls.xpath('//span[@class="ss03"]/a/text()|//div[@class="yc_tit"]/p/a/text()')[0]
        else:
            source = ""
        # 栏目路径
        if len(htmls.xpath('//div[@class="theLogo"]/div/a[2]/text()|//div[@class="h_nav"]/a[2]/text()')) > 0:
            lm2 = htmls.xpath('//div[@class="theLogo"]/div/a[2]/text()|//div[@class="h_nav"]/a[2]/text()')[0]
        else:
            lm2 = ""
        if len(htmls.xpath(
                '//div[@class="speNav js_crumb"]/a[1]/text()|//div[@class="h_nav"]/a[1]/text()|//div[@class="theLogo"]/div/a[1]/text()')) > 0:
            lm1 = htmls.xpath(
                '//div[@class="speNav js_crumb"]/a[1]/text()|//div[@class="h_nav"]/a[1]/text()|//div[@class="theLogo"]/div/a[1]/text()')[
                0]
        else:
            lm1 = ""
        lmlj = lm1 + ";" + lm2
        # 参与人数
        if len(htmls.xpath('//div[@class="box03"]/h5/span/a/em/text()')) > 0:
            cy_num = htmls.xpath('//div[@class="box03"]/h5/span/a/em/text()')[0]
        else:
            cy_num = ""
        # 评论数
        if len(htmls.xpath('//div[@class="box03"]/h5/a/em/text()')) > 0:
            pl_num = htmls.xpath('//div[@class="box03"]/h5/a/em/text()')[0]
        else:
            pl_num = ""
        # 编者
        if len(htmls.xpath('//div[@id="artical_sth2"]/p[1]/text()')) > 0:
            bz = htmls.xpath('//div[@id="artical_sth2"]/p[1]/text()')
        else:
            bz = ""
        # 成稿时间
        if len(htmls.xpath('//div[@id="artical_sth"]/p/span[1]/text()')) > 0:
            cg_time = htmls.xpath('//div[@id="artical_sth"]/p/span[1]/text()')[0]
        else:
            cg_time = ""
        # 推荐数
        if len(htmls.xpath('//div[@id="left_dz"]/span/text()')) > 0:

            tj_num = htmls.xpath('//div[@id="left_dz"]/span/text()')[0]
        else:
            tj_num = ""
        # 图片
        if len(htmls.xpath(
                '//p[@class="detailPic"]/img/@src|//div[@class="yc_con_txt"]/p/img/@src|//div[@id="main_content"]/p/img/@src|//div[@class="box02"][1]/img/@src')
        ) > 0:
            img_list = htmls.xpath(
                '//p[@class="detailPic"]/img/@src|//div[@class="yc_con_txt"]/p/img/@src|//div[@id="main_content"]/p/img/@src|//div[@class="box02"][1]/img/@src')[
                0]
        else:
            img_list = ""
        zwwbhtml = driver.find_element_by_xpath('//div[@id="main_content"]').get_attribute('outerHTML')
        # zwwbhtml.get_attribute('outerHTML')
        # zwwbhtml = htmls.xpath('//div[@id="main_content"]')

        # print("============>>>>>>>>>>>>>", zwwbhtml)
        # print(zwwbhtml)
        img_url = '//p[@class="detailPic"]/img'
        st = self.process_image_src(zwwbhtml, img_url)
        ZWNR = "".join(st)
        # print('=ZWNR===', ZWNR, type(ZWNR))
        urlpath = response.url  # 这是那个  ---http://news.ifeng.com/a/20190108/60227925_0.shtml
        WEBSITE = r'ifeng/' + lm2 + '/html/'
        filename = os.path.join(WEBSITE, urlpath.split('/')[-1].strip('/'))
        file_dir = os.path.dirname(filename)
        os.makedirs(file_dir, exist_ok=True)
        with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(driver.page_source)

        # 标题
        item['BTIT'] = title
        # 参与人数
        item['CYRS'] = cy_num
        # 评论数
        item['PLS'] = pl_num
        # 新闻来源
        item['XWLY'] = source
        # 栏目路径
        item['LMLJ'] = lmlj
        # 编者
        item['BZ'] = bz
        # 成稿时间
        item['CGSJ'] = cg_time.replace("年", "-").replace("月", "-").replace('日', '-')
        # 采集时间
        item['CJSJ'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 正文文本
        item['ZWWB'] = cont.replace("\n", "").replace("\r", "")
        # 正文内容
        item['ZWNR'] = ZWNR.replace("<html><body>", "").replace("</body></html>", "")
        # 推荐数
        item['TJS'] = tj_num
        # # 原始网页链接
        item['YS_URL'] = filename
        # # 处理网页链接
        item['CL_URL'] = filename
        # 缩略图链接
        item['TP_URL'] = img_list
        # url
        item['URL'] = urlpath
        item['LMLJ2'] = lm2
        driver.close()
        # print(item)
        yield item

    def parse_item(self, response):
        '''
        该方法用于处理列表页
        作用是将日期为20180601以后的四个专题
        新闻列表页获取到，之后从列表页中使用
        xpath将详情页url获取到，再将详情页的url进行
        第二次清洗过滤出符合需求的详情页url，在将详情页
        的url交给parse_datel方法处理
        '''
        num = "".join(response.url).split("/")[5]
        if int(num) >= 20180601:
            # 新闻列表页
            news_list_url = response.xpath('//div[@class="newsList"]/ul')
            if news_list_url:
                news_url = response.xpath('//div[@class="newsList"]/ul/li/a/@href').extract()
                for new_url in news_url:
                    pattern = re.compile(r'^http://(.*)/a/(\d+)/(.*).shtml$')
                    datel_url = pattern.match(new_url)
                    datel_url = datel_url.group(0)
                    yield scrapy.Request(datel_url, callback=self.parse_datel, dont_filter=True)
