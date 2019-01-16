# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ZaoBaoItem(scrapy.Item):
    title = scrapy.Field()


class ZaoBaoUrlItem(scrapy.Item):
    urls = scrapy.Field()

# class ZaoBaoUrlItem(scrapy.Item):
#     url = scrapy.Field()
#     breadcrumb = scrapy.Field()


class NewsDetailItem(scrapy.Item):
    BT = scrapy.Field()
    XWLY = scrapy.Field()
    ZZLY = scrapy.Field()
    LMLJ = scrapy.Field()
    BZ = scrapy.Field()
    CGSJ = scrapy.Field()
    CJSJ = scrapy.Field()
    RKSJ = scrapy.Field()
    YDL = scrapy.Field()
    ZZL = scrapy.Field()
    DZL = scrapy.Field()
    ZWWB = scrapy.Field()
    ZWNR = scrapy.Field()
    YS_URL = scrapy.Field()
    CL_URL = scrapy.Field()
    TP_URL = scrapy.Field()

