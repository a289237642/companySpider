# -*- coding: utf-8 -*-
import scrapy
from gaoxueya.items import DoctorItem


class SpiderhypertensionSpider(scrapy.Spider):
    name = 'spiderhypertension'
    allowed_domains = ['ask.familydoctor.com.cn']
    # start_url = ['http://ask.familydoctor.com.cn/did/63/?page=']
    page = 1
    url = "http://ask.familydoctor.com.cn/did/63/?page="
    start_urls = [url + str(page)]

    def handlesQuestion(self, doctors):
        ss = doctors.split()
        # doctor=ss[0]
        # level=ss[1]
        # return doctor,level
        return ss

    def parse_info(self, response):

        doctors = response.xpath('//dl[@class="answer-info-cont"]/dt/a/p/text()').extract()
        # print(doctors)
        # 点赞数
        good_num = response.xpath(
            '//div[@class="main lfloat main-small"]/div[2]/ul/li/div[2]/dl/dt/div/i[1]/text()').extract()
        # 踩数量
        bad_num = response.xpath(
            '//div[@class="main lfloat main-small"]/div[2]/ul/li/div[2]/dl/dt/div/i[2]/text()').extract()
        # 回答内容
        # answers = response.xpath('//p[@class="answer-words"]/text()').extract()[0]
        answers = response.xpath('//p[@class="answer-words"]/text()').extract()
        # 回答时间
        # answers_time = response.xpath(
        # '//div[@class="main lfloat main-small"]/div[2]/ul/li/div[2]/dl/dd/div//span/text()').extract()
        answers_time = response.xpath('//span[@class="icon-time"]/text()').extract()
        for i in range(len(doctors)):
            item = DoctorItem()
            if len(doctors) > 0:
                li = self.handlesQuestion(doctors[i])
                item['doctor'] = li[0]
                if len(li) == 1:
                    item['level'] = ""
                    item['good_num'] = good_num[0]
                    item['bad_num'] = bad_num[0]
                else:
                    item['level'] = li[1]
                    item['good_num'] = good_num[i]
                    item['bad_num'] = bad_num[i]
                item['answers'] = answers[i].strip()
                item['answers_time'] = answers_time[i]
                item['wt_url'] = response.url
            yield item

    def parse(self, response):
        # 得到所有问题的链接
        links = response.xpath("//div[@class='cont faq-list']/dl/dt/p/a/@href").extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_info)

        if self.page < 3738:
        # if self.page < 2:
            self.page += 1
            new_url = self.url + str(self.page)
            yield scrapy.Request(new_url, callback=self.parse)
