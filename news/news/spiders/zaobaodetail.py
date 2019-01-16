# -*- coding: utf-8 -*-

import os
from uuid import uuid4
from datetime import datetime
from urllib.parse import urlparse

import scrapy
import redis
import requests

from news.items import NewsDetailItem


redis_host = '192.168.1.114'

PREFIX_DIR = ''
WEBSITE_DIR = 'zaobao'
HTML_DIR = 'html'
IMAGE_DIR = 'image'



class ZaobaodetailSpider(scrapy.Spider):
    name = 'zaobaodetail'
    # allowed_domains = ['www.zaobao.com']
    website = 'http://www.zaobao.com'

    def start_requests(self):
        for url in self.get_urls():
            u = url.decode('utf8')
            metadata = {}
            if u.startswith('/realtime/china/story'):
                metadata['lmlj'] = '首页;即时报道;中港台即时',
            elif u.startswith('/realtime/world/story'):
                metadata['lmlj'] = '首页;即时报道;国际即时',
            elif u.startswith('/news/china/story'):
                metadata['lmlj'] = '首页;新闻;中国新闻'
            elif u.startswith('/news/world/story'):
                metadata['lmlj'] = '首页;新闻;国际新闻'
            else:
                continue

            yield scrapy.Request(self.website + u, meta={'zaobao': metadata})

    def parse(self, response):
        item = NewsDetailItem()
        item['LMLJ'] = response.meta['zaobao']['lmlj']
        item['CJSJ'] = datetime.now().strftime('%Y-%m-%d %H:%M')

        item['BT'] = response.xpath('//div[@class="body-content"]/h1/text()').extract_first()

        trackme = response.xpath('//aside[@class="trackme"]')
        published_element = trackme.xpath('span[contains(@class, "datestamp date-published")]')
        if published_element:
            published_date = trackme.xpath('span[contains(@class, "datestamp date-published")]/text()[2]').extract_first()
            published_time = trackme.xpath('span[contains(@class, "datestamp date-published")]/em/text()').extract_first()
            dt = published_date + ' ' + published_time
            published_datetime = self.process_datetime(dt)
            print(published_datetime)
            item['CGSJ'] = published_datetime

        # updated_element = trackme.xpath('span[contains(@class, "datestamp date-updated")]')
        contributor_element = trackme.xpath('span[contains(@class, "contributor")]')
        if contributor_element:
            contributor = contributor_element.xpath('a/text()').extract_first()
            item['BZ'] = contributor

        publication_element = trackme.xpath('span[span[@class="publication"]]')
        if publication_element:
            publication = publication_element.xpath('span/a/text()')[-1].extract()
            item['XWLY'] = publication

        item['ZWWB'] = response.xpath('//div[@id="FineDining"]').extract_first()
        item['ZWNR'] = response.xpath('//article[@id="MainCourse"]').extract_first()

        url_parser = urlparse(response.url)
        subject_path = os.path.dirname(url_parser.path)
        rel_html_dir = os.path.join(WEBSITE_DIR, HTML_DIR) + subject_path
        rel_image_dir = os.path.join(WEBSITE_DIR, IMAGE_DIR) + subject_path

        html_name = url_parser.path.split('/')[-1]

        os.makedirs(rel_html_dir, exist_ok=True)
        os.makedirs(rel_image_dir, exist_ok=True)

        self.write_html(response.body, rel_html_dir, html_name)

        item['YS_URL'] = rel_html_dir + '/' + html_name
        item['CL_URL'] = rel_html_dir + '/' + html_name

        img_url = response.xpath('//div[@class="loadme"]/picture/source/@data-srcset').extract_first()
        if img_url:
            item['TP_URL'] = self.download_img(img_url, rel_image_dir)

        yield item

    def write_html(self, body, rel_path, name):
        path = PREFIX_DIR + '/' + rel_path + '/' + name if PREFIX_DIR else rel_path + '/' + name

        with open(path, 'wb') as f:
            f.write(body)

    def download_img(self, url, dirname):
        path = dirname + '/' + str(uuid4()) + '.jpg'

        try:
            r = requests.get(url, timeout=50)
            with open(path, 'wb') as f:
                f.write(r.content)
                return path
        except Exception as e:
            pass

    def get_urls(self):
        self.client = redis.Redis(host=redis_host)
        data = self.client.smembers('zaobao_url')
        # print(list(data).sort())
        # print(data)
        # print(len(data))
        # print(type(data))
        return data

    def process_datetime(self, dt):
        return datetime.strptime(dt, '%Y年%m月%d日 %I:%M %p').strftime('%Y-%m-%d %H:%M')

if __name__ == '__main__':
    s = ZaobaodetailSpider()
    urls = s.get_urls()
    # for url in urls:
    #     print(url)
    #     print(url.decode('utf8'))