from doctor.items import DoctorItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DoctorlistSpider(CrawlSpider):
    name = 'doctorList'

    # scrapy-redis
    redis_key = 'myspider:start_urls'
    allowed_domains = ['ask.39.net']
    # 规则爬虫
    rules = (
        Rule(LinkExtractor(allow=r'question/(\d+).html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print('response.url===========', response.url)
        item = DoctorItem()
        div = response.xpath('//div[@class="sele_all marg_top"] | //div[@class="sele_all"]')
        for dd in div:
            # 医生姓名
            name = dd.xpath('./div[1]/div[2]/p[@class="doc_xinx"]/span[1]/text()').extract()
            item['name'] = ''.join(name)
            # 医生级别
            level = dd.xpath('./div[1]/div[2]/p[@class="doc_xinx"]/span[2]/text()').extract()
            item['level'] = ''.join(level)
            # 工作单位
            company = dd.xpath('./div[1]/div[2]/p[@class="doc_xinx"]/span[3]/text()').extract()
            # 擅长的领域
            good = dd.xpath('./div[1]/div[2]/p[@class="doc_sc"]/span/text()').extract()
            if len(div.xpath(".//span[@class='doc_yshi']/text()")) > 1:
                # 医院
                item['company'] = ''.join(company)
            else:
                item['company'] = ''
            if len(div.xpath(".//p[@class='doc_sc']/span/text()")) > 0:
                # 擅长
                item['good'] = ''.join(good)
            else:
                item['good'] = ''
            # 回答答案
            detail = dd.xpath('./p/text()').extract()
            item['detail'] = ''.join(detail)
            # 回答时间
            time = dd.xpath('./div[@class="doc_t_strip"]/div[1]/p/text()').extract()
            item['time'] = ''.join(time[0])

            item['link'] = response.url
            yield item
