# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class DoctorItem(Item):
    # 医生姓名
    name = Field()
    # 医生级别
    level = Field()
    # 工作单位
    company = Field()
    # 擅长的领域
    good = Field()
    # 回答答案
    detail = Field()
    # 回答时间
    time = Field()
    # 问题链接
    link = Field()
    # 帮助人数
    helpNum = Field()

    crawled = Field()
    spider = Field()


class DoctorLoader(ItemLoader):
    default_item_class = DoctorItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
