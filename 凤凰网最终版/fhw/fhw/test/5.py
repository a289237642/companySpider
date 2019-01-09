# import requests
#
# a = requests.get(
#     'http://dps.kdlapi.com/api/getdps/?orderid=924667075915495&num=10&pt=1&sep=1').text.split("\n")
# for i in a:
#     print(i)

from selenium import webdriver

# import os
#
url = "http://news.ifeng.com/a/20190104/60223969_0.shtml"


#
#
def handlejs(url):
    driver = webdriver.Chrome()
    driver.get(url)
    # 标题
    BT = driver.find_element_by_xpath(
        '//div[@id="titL"]/h1/text()|//div[@class="yc_tit"]/h1/text()|//h1[@id="artical_topic"]').text
    # 编者
    # BZ = driver.find_element_by_xpath(
    #     '//div[@id="artical_sth2"]/p[1]/text()|//div[@id="main_content"]/p[12]/text()|//span[@class="ss04"]/span').text
    # 正文文本
    ZWWB=driver.find_element_by_xpath('//div[@id="main_content"]/p').text
    # 参与人数
    CYRS = driver.find_element_by_xpath('//em[@class="js_joinNum"][1]').text
    # 评论数
    PLS = driver.find_element_by_xpath('//em[@class="js_cmtNum"][1]').text
    # 推荐数
    TJS = driver.find_element_by_xpath('//div[@id="left_dz"]/span').text

    driver.close()
    return BT, CYRS, PLS, TJS,ZWWB,


BT, CYRS, PLS, TUS,ZWWB = handlejs(url)
print(ZWWB)

# # driver = webdriver.Chrome()
# driver.get(url)
#
# CYRS = driver.find_element_by_xpath('//em[@class="js_joinNum"][1]').text
# PLS = driver.find_element_by_xpath('//em[@class="js_cmtNum"][1]').text
# with open("1.html", 'w', encoding='utf-8', errors='ignore')as f:
#     f.write(driver.page_source)
