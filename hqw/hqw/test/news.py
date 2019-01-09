# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fhw.items import FhwItem
from selenium import webdriver
from datetime import datetime
import re
from lxml import etree

PREFIX = r'Z:\\'
WEBSITE = r'ifeng'


class NewsSpider(CrawlSpider):
	name = 'news'
	allowed_domains = ['news.ifeng.com']
	start_urls = ['http://news.ifeng.com/listpage/11490/20181231/1/rtlist.shtml','http://news.ifeng.com/listpage/11528/0/1/rtlist.shtml','http://news.ifeng.com/listpage/11574/0/1/rtlist.shtml','http://news.ifeng.com/listpage/7609/0/1/rtlist.shtml']

	rules = (
		Rule(LinkExtractor(allow=r'rtlist.shtml$'), callback='parse_item',follow=True),
	)


	

	def parse_datel(self, response):
		'''
		该方法用于处理详情页信息
		通过xpath定位出相应的数据
		'''
		print("====", response.url)
		driver = webdriver.Chrome()
		driver.get(response.url)
		htmls = etree.HTML(driver.page_source)
		item = FhwItem()
		
		# 文章标题
		title = htmls.xpath('//div[@class="yc_tit"]/h1/text()|//div[@id="artical"]/h1/text()')[0]
		# 文章内容
		cont = htmls.xpath('//div[@id="main_content"]/p/text()|//div[@id="main_content"]/text()')
		# 新闻来源
		source = htmls.xpath('//span[@class="ss03"]/a/text()|//div[@class="yc_tit"]/p/a/text()')[0]
		# 栏目路径
		lm2 = htmls.xpath('//div[@class="theLogo"]/div/a[2]/text()|//div[@class="h_nav"]/a[2]/text()')[0]
		lm1 = htmls.xpath('//div[@class="speNav js_crumb"]/a[1]/text()|//div[@class="h_nav"]/a[1]/text()|//div[@class="theLogo"]/div/a[1]/text()')[0]
		lmlj = lm1+";"+lm2
		# 参与人数
		cy_num = htmls.xpath('//div[@class="box03"]/h5/span/a/em/text()')[0]
		# 评论数
		pl_num = htmls.xpath('//div[@class="box03"]/h5/a/em/text()')[0]
		# 编者
		bz = htmls.xpath('//div[@id="artical_sth2"]/p[1]/text()')
		# 成稿时间
		cg_time = htmls.xpath('//div[@id="artical_sth"]/p/span[1]/text()')[0]
		# 推荐数
		tj_num = htmls.xpath('//div[@id="left_dz"]/span/text()')[0]
		# 图片
		img_list = htmls.xpath('//p[@class="detailPic"]/img/@src|//div[@class="yc_con_txt"]/p/img/@src|//div[@id="main_content"]/p/img/@src|//div[@class="box02"][1]/img/@src')


		# 标题
		item['BTIT'] = title
		# 参与人数
		item['CYRS'] = cy_num
		# 评论数
		item['PLS'] = pl_num
		# 新闻来源
		item['XWLY'] = source
		# 栏目路径
		item['LMLJ'] = lmlj
		# 编者
		item['BZ'] = bz
		# 成稿时间
		item['CGSJ'] = cg_time
		# 采集时间
		item['CJSJ'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		# # 阅读量
		# YDL = scrapy.Field()
		# # 转载量
		# ZZL = scrapy.Field()
		# # 点赞量
		# DJL = scrapy.Field()
		# 正文内容
		item['ZWNR'] = cont
		# 推荐数
		item['TJS'] = tj_num
		# # 原始网页链接
		# YS_URL = scrapy.Field()
		# # 处理网页链接
		# CL_URL = scrapy.Field()
		# # 缩略图链接
		# TP_URL = scrapy.Field()



		driver.close()
		yield item





	def parse_item(self, response):
		'''
		该方法用于处理列表页
		作用是将日期为20180601以后的四个专题
		新闻列表页获取到，之后从列表页中使用
		xpath将详情页url获取到，再将详情页的url进行
		第二次清洗过滤出符合需求的详情页url，在将详情页
		的url交给parse_datel方法处理
		'''
		num = "".join(response.url).split("/")[5]
		if int(num)>=20180601:
			# 新闻列表页
			news_list_url = response.xpath('//div[@class="newsList"]/ul')
			if news_list_url:
				news_url = response.xpath('//div[@class="newsList"]/ul/li/a/@href').extract()
				for new_url in news_url:
					pattern = re.compile(r'^http://(.*)/a/(\d+)/(.*).shtml$')
					datel_url = pattern.match(new_url)
					datel_url = datel_url.group(0)
					yield scrapy.Request(datel_url,callback=self.parse_datel,dont_filter=True)

