# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymysql, requests
from scrapy.conf import settings
from datetime import datetime


class FhwPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DBNAME'],
            port=settings['MYSQL_PORT']
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        # 图片下载
        path_url = item['TP_URL']
        print("===", path_url)
        WEBSITE = r'ifeng/' + item['LMLJ2'] + ''
        if not os.path.exists(WEBSITE + "/images/"):
            os.makedirs(WEBSITE + "/images/")
        image_path = WEBSITE + "/images/" + path_url.split("/")[-1]

        if not os.path.exists(image_path):
            response = requests.get(path_url)
            if response.status_code == 200:
                with open(image_path, "wb")as f:
                    f.write(response.content)
        self.connect.ping(reconnect=True)
        self.cursor.execute(
            "insert into lg2(BTIT,CYRS,PLS,XWLY,LMLJ,BZ,CGSJ,CJSJ,ZWWB,ZWNR,TJS,YS_URL,CL_URL,TP_URL,RKSJ,URL) "
            "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [item.get('BTIT'), item.get('CYRS'), item.get('PLS'), item.get('XWLY'), item.get('LMLJ'), item.get('BZ'),
             item.get('CGSJ'),
             item.get('CJSJ'), item.get('ZWWB'), item.get('ZWNR'), item.get('TJS'), item.get('YS_URL'), item['CL_URL'],
             image_path,
             datetime.now(), item['URL']])
        self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close();
