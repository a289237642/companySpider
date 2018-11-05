# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class SickItem(Item):
    # 问题类目一
    catOne = Field()
    # 问题类目二
    catTwo = Field()
    # 问题类目三
    catThree = Field()
    # 问题类目四
    catFour = Field()

    # 问题标题
    title = Field()
    # 患者性别
    gender = Field()
    # 年龄
    age = Field()
    # 发病时间
    startTime = Field()
    # 问题描述
    question = Field()
    # 提问时间
    questionTime = Field()
    # 问题标签
    questionTag = Field()
    # 问题链接
    questionUrl = Field()

    crawled = Field()
    spider = Field()


class SickLoader(ItemLoader):
    default_item_class = SickItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
