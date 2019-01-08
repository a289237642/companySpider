# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymysql
from scrapy import log
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import requests
import json
#图片下载
class MapSpiderImagePipeline(object):
    def process_item(self, item, spider):
        img_url = item['bigpicurl']
        num = "".join(img_url).split('/')[7]
        numa = "".join(img_url).split('/')[8]
        objid = item['pictureid']
        image_path = "b_" + str(objid) + str(num) + "_" + str(numa) + ".jpg"
        if not os.path.exists("./Image"):
            os.makedirs("./Image")
        if not os.path.exists(image_path):
            response = requests.get(img_url)
            print("response================",response)
            if response.status_code == 200:
                with open("./Image/"+image_path,'wb') as f:
                    f.write(response.content)
            item['physicalname'] = image_path
        return item



# 保存成JSON格式
class MapSpiderPipeline(object):
    def open_spider(self,spider):
        self.file = open(spider.name+".json","a+",encoding="utf-8")

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item), ensure_ascii=False) + "\n")
        return item

    def close_spider(self,spider):
        self.file.close()

# 将数据保存到数据库
import psycopg2
import scrapy
import logging
logger = logging.getLogger('CrawlfangImagePipeline')
class CrawlfangPipeline(object):
    def __init__(self):
        self.conn = psycopg2.connect(database="webspider", user="gpadmin", password="gpadmin", host="192.168.0.2", port="5432")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        title = item.get('title')
        bigpicurl = item.get('bigpicurl')
        content = item.get('content')
        physicalname = item.get('physicalname')
        pictureid = item.get('pictureid')

        try:
            insert_sql = """
                 insert into beepic(title,bigpicurl,content,physicalname,pictureid)
                 values (%s,%s,%s,%s,%s)
            """
            self.cursor.execute(insert_sql,(title,bigpicurl,content,physicalname,pictureid))
            self.conn.commit()
            log.msg("Data added to PostgreSQL database!",
                    level=log.DEBUG, spider=spider)
        except Exception as e:
            print('insert record into table failed')
            print (e)
        return item




