#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from scrapy.settings import Settings
from selenium import webdriver

from news.config import BASEDIR

from selenium.webdriver.remote.webelement import WebElement

url = "http://news.ifeng.com/a/20190104/60223969_0.shtml"

path = os.path.join(BASEDIR, 'drivers', 'chromedriver')
driver = webdriver.Chrome(executable_path=path)
driver.get(url)

num = driver.find_element_by_xpath('//em[@class="js_joinNum"][1]')
print(num)
print(num.text)
# print(num.get_attribute('innerHTML'))
print(num.get_attribute('outerHTML'))
driver.close()
