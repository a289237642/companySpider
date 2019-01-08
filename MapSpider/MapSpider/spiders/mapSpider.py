# -*- coding: utf-8 -*-
import re
import scrapy
#from MapSpider.get_date_tools.get_pictureid import ssh_postpre

from MapSpider.items import MapspiderItem

class MapspiderSpider(scrapy.Spider):
    name = 'mapSpider'
    allowed_domains = ['home.fang.com/album/ideabook']

    start_urls = [
        'http://home.fang.com/album/ideabook/?page=96',
        #'http://home.fang.com/album/ideabook/?page=97',
    ]


    def parse_detail(self,response):
        print("正在爬取=================", response.url)
        item = response.meta["item"]
        # 图片标题
        title = response.xpath('//div[@class="tit"]/h2/text()').extract()
        title = "".join(title)
        item['title'] = title
        # 大图URL
        bigpicurls = response.xpath('//div[@class="photo_h"]/i/a/img/@src | //div[@class="photo_s"]/i/a/img/@src').extract()
        # 图片说明
        content_info = response.xpath('//div[@class="photo_h"]/p | //div[@class="photo_s"]/p').extract()
        #定义list用于存放content
        contents = []
        #拼接content
        for cont in content_info:
            pattern = re.compile('</?p[^>]*>')
            contx = pattern.sub('', cont)
            pattern = re.compile('</?a[^>]*>')
            conts = pattern.sub('', contx)
            item['content'] = conts
            contents.append(conts)

        for i in range(len(bigpicurls)):
            item['bigpicurl'] = "http:" + bigpicurls[i]
            item['content'] = contents[i]

            yield item


    def parse(self, response):
        print(response.url)
        # 详情页url
        urls = response.xpath('//div[@class="photo_list"]/ul/li/ol/span/a/@href').extract()
        items = []
        for url in urls:
            item = MapspiderItem()
            #获取详情页id
            pictureid = "".join(url).split('/')[-2]
            item['detailsurl'] = url
            item['pictureid'] = pictureid
            items.append(item)
        for item in items:
            #拼接详情页url
            details_url = 'http:' + item['detailsurl']
            yield scrapy.Request(details_url, callback=self.parse_detail, meta={"item": item}, dont_filter=True)






