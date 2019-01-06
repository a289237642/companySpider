# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymysql, requests
from scrapy.conf import settings
from datetime import datetime

PREFIX = r'Z:\\'
WEBSITE = r'ifeng'

"""
 filename = os.path.join(PREFIX, WEBSITE, urlpath.strip('/'))
        file_dir = os.path.dirname(filename)
        os.makedirs(file_dir, exist_ok=True)
        with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(driver.page_source)
"""


# class ImagePipeline(object):
#     def process_item(self, item, spider):
#         # 图片下载
#         path_url = item['TP_URL']
#         print("===", path_url)
#         if not os.path.exists("PREFIX/Images/"):
#             os.makedirs("PREFIX/Images/")
#         image_path = "PREFIX/Images/" + path_url.split("/")[-1]
#
#         if not os.path.exists(image_path):
#             response = requests.get(path_url)
#             if response.status_code == 200:
#                 with open(image_path, "wb")as f:
#                     f.write(response.content)
#         return item


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
        # print("=======item", item)

        # 图片下载
        path_url = item['TP_URL']
        print("===", path_url)
        if not os.path.exists(PREFIX+"/Images/"):
            os.makedirs(PREFIX+"/Images/")
        image_path = PREFIX+"/Images/" + path_url.split("/")[-1]

        if not os.path.exists(image_path):
            response = requests.get(path_url)
            if response.status_code == 200:
                with open(image_path, "wb")as f:
                    f.write(response.content)

        try:
            self.cursor.execute(
                "insert into news(BTIT,CYRS,PLS,XWLY,LMLJ,ZWWB,ZWNR,TP_URL,BZ,TJS,CJSJ,YS_URL,CL_URL,RKSJ,CGSJ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [item['BTIT'], item['CYRS'], item['PLS'], item['XWLY'], item['LMLJ'], item['ZWWB'], item['ZWNR'],
                 image_path, item['BZ'], item['TJS'], item['CJSJ'], item['YS_URL'], item['CL_URL'], datetime.now(),
                 item['CGSJ']])
            self.connect.commit()
        except Exception as error:
            print(error)
        return item

    def close_spider(self, spider):
        self.connect.close();
