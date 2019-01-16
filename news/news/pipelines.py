# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

import redis
import pymysql

from scrapy.conf import settings


class NewsPipeline(object):
    def process_item(self, item, spider):
        return item


class ZaoBaoUrlPipeline(object):
    # def __init__(self, redis_host, redis_port, redis_db):
    # def __init__(self):
    #     self.redis_host = settings.get('redis_host'),
    #     self.redis_port = settings.get('redis_port'),
    #     self.redis_db = settings.get('redis_db')
    #     print('__init__' * 50)
    #     print(self.redis_host)
    #     print(settings['ITEM_PIPELINES'])
    #     print(settings['redis_host'])

    # @classmethod
    # def from_crawler(cls, crawler):
    #     print('^' * 50)
    #     print(crawler.settings)
    #     print(crawler.settings.get('redis_host'))
    #     return cls(
    #         redis_host=crawler.settings.get('redis_host'),
    #         redis_port=crawler.settings.get('redis_port'),
    #         redis_db=crawler.settings.get('redis_db')
    #     )

    def open_spider(self, spider):
        # redis_host = spider.settings.get('redis_host'),
        # redis_port = spider.settings.get('redis_port'),
        # redis_db = spider.settings.get('redis_db')
        #
        if spider.name == 'zaobao':
            self.client = redis.Redis(host='192.168.1.114')
        if spider.name == 'zaobaodetail':
            self.conn = pymysql.connect(
                host='192.168.1.114',
                user='udsafe',
                password='udsafe',
                database='newsinfo',
                charset='utf8')
            self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # print('process_item' * 50)
        if spider.name == 'zaobao':
            urls = item.get('urls')
            self.client.sadd('zaobao_url', *urls)
        elif spider.name == 'zaobaodetail':
            item['RKSJ'] = datetime.now().strftime('%Y-%m-%d %H:%M')

            self.cursor.execute(
                "insert into hxf_copy1(BT,XWLY,LMLJ,BZ,CGSJ,CJSJ,ZWWB,ZWNR,YS_URL,CL_URL,TP_URL,RKSJ) "
                "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [item['BT'], item.get('XWLY'),
                 item['LMLJ'], item.get('BZ'), item.get('CGSJ'),
                 item['CJSJ'], item['ZWWB'], item['ZWNR'],
                 item['YS_URL'], item['CL_URL'], item.get('TP_URL'),
                 item['RKSJ']])
            self.conn.commit()

            return item

        else:
            return item
        # return item