# -*- coding: utf-8 -*-

from datetime import datetime

import scrapy
import requests

from news.items import ZaoBaoUrlItem


links = [
    {
        'url': 'http://www.zaobao.com/realtime/china?page={page}',
        # 'breadcrumb': '首页;即时报道;中港台即时',
        'page': 0
    },
    {
        'url': 'http://www.zaobao.com/realtime/world?page={page}',
        # 'breadcrumb': '首页;即时报道;国际即时',
        'page': 0
    },
{
        'url': 'http://www.zaobao.com/news/china?page={page}',
        # 'breadcrumb': '首页;即时报道;国际即时',
        'page': 0
    },
{
        'url': 'http://www.zaobao.com/news/world?page={page}',
        # 'breadcrumb': '首页;即时报道;国际即时',
        'page': 0
    },
]


class ZaoBaoSpider(scrapy.Spider):
    name = 'zaobao'
    allowed_domains = ['zaobao.com']

    date_start = datetime.strptime('20180531', '%Y%m%d')

    def start_requests(self):
        for link in links:
            url = link.get('url')
            page = link.get('page')
            url = url.format(page=page)
            link['page'] = page + 1

            yield scrapy.Request(url, meta={'link': link})

    def parse(self, response):
        items = response.xpath('//div[@class=" row list"]')
        link = response.meta.get('link')
        url = link.get('url')
        page = link.get('page')
        url = url.format(page=page)
        link['page'] = page + 1

        is_continue = True

        urls = ZaoBaoUrlItem()

        ret = []
        for i in items:
            href = i.xpath('div/a/@href').extract_first()

            try:
                time_str = href.split('/')[-1].split('-')[0][5:]
                print(time_str)
                date_cur = datetime.strptime(time_str, '%Y%m%d')
                if date_cur <= self.date_start:
                    is_continue = False

                # 如果执行正常，就加到列表中，否则不加入列表
                ret.append(href)

            except Exception as e:
                continue

        urls['urls'] = ret

        if is_continue:
            yield scrapy.Request(url, meta={'link': link})

        yield urls
