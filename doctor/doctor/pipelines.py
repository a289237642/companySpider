# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.conf import settings
from datetime import datetime


class ExamplePipeline(object):
    def process_item(self, item, spider):
        # 当前爬取的时间
        item["crawled"] = datetime.utcnow()
        # 爬虫的名称
        item["spider"] = spider.name + "_001"
        return item


class DoctorPipeline(object):
    def process_item(self, item, spider):

        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name

        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DBNAME']
        port = settings['MYSQL_PORT']

        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, port=port)

        cue = con.cursor()

        try:
            cue.execute(
                "insert into doctor39(name,level,company,good,detail,time,link,helpNum) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                [item['name'], item['level'], item['company'], item['good'], item['detail'], item['time'],
                 item['link'],item['helpNum']])
        except Exception as e:
            print('Insert error:', e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item
