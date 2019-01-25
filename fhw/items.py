# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FhwItem(scrapy.Item):
    # 标题
    BTIT = scrapy.Field()
    # 参与人数
    CYRS = scrapy.Field()
    # 评论数
    PLS = scrapy.Field()
    # 新闻来源
    XWLY = scrapy.Field()
    # 转载来源
    ZZLY = scrapy.Field()
    # 栏目路径
    LMLJ = scrapy.Field()
    # 编者
    BZ = scrapy.Field()
    # 成稿时间
    CGSJ = scrapy.Field()
    # 采集时间
    CJSJ = scrapy.Field()
    # 入库时间
    RKSJ = scrapy.Field()
    # 阅读量
    YDL = scrapy.Field()
    # 转载量
    ZZL = scrapy.Field()
    # 点赞量
    DJL = scrapy.Field()
    # 正文文本
    ZWWB = scrapy.Field()
    # 正文内容
    ZWNR = scrapy.Field()
    # 推荐数
    TJS = scrapy.Field()
    # 原始网页链接
    YS_URL = scrapy.Field()
    # 处理网页链接
    CL_URL = scrapy.Field()
    # 缩略图链接
    TP_URL = scrapy.Field()

    # 专题
    LMLJ2 = scrapy.Field()

    URL = scrapy.Field()
