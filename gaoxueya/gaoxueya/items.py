# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoctorItem(scrapy.Item):
    doctor = scrapy.Field()
    level=scrapy.Field()
    good_num = scrapy.Field()
    bad_num = scrapy.Field()
    answers = scrapy.Field()
    answers_time = scrapy.Field()
    wt_url = scrapy.Field()


