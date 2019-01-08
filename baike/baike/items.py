# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaikeItem(scrapy.Item):
    # 主表
    MC = scrapy.Field()
    YWMC = scrapy.Field()
    QTMC = scrapy.Field()
    BKLY = scrapy.Field()
    GXSJ = scrapy.Field()
    CJSJ = scrapy.Field()
    RKSJ = scrapy.Field()
    FLLJ = scrapy.Field()
    YS_URL = scrapy.Field()
    CL_URL = scrapy.Field()
    TP_URL = scrapy.Field()
    URL = scrapy.Field()
    BKJS = scrapy.Field()
    # 从表
    BKID = scrapy.Field()
    SXMC = scrapy.Field()
    SXLX = scrapy.Field()
    SXZ = scrapy.Field()
    XH = scrapy.Field()
