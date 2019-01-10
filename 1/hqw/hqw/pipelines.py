# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql, requests, os
from scrapy.conf import settings
from datetime import datetime


class HqwPipeline(object):

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
        WEBSITE = r'huanqiu/' + item['catTwo'] + ''
        if not os.path.exists(WEBSITE + "/images/"):
            os.makedirs(WEBSITE + "/images/")
        image_path = WEBSITE + "/images/" + path_url.split("/")[-1]

        if not os.path.exists(image_path):
            response = requests.get(path_url)
            if response.status_code == 200:
                with open(image_path, "wb")as f:
                    f.write(response.content)
        try:

            self.cursor.execute(
                "insert into news_hqw(BTIT,CYRS,XWLY,LMLJ,BZ,CGSJ,CJSJ,ZWWB,ZWNR,YS_URL,CL_URL,TP_URL,RKSJ,URL) "
                "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [item['BTIT'], item['CYRS'], item['XWLY'], item['LMLJ'], item['BZ'], item['CGSJ'],
                 item['CJSJ'], item['ZWWB'], item['ZWNR'], item['YS_URL'], item['CL_URL'], image_path,
                 datetime.now(), item['URL']])
            self.connect.commit()
        except Exception as error:
            print(error)
        return item

    def close_spider(self, spider):
        self.connect.close();
