from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# url = "http://news.ifeng.com/a/20190104/60223969_0.shtml"
url = 'http://www.baidu.com'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)

driver.get(url)

aa = driver.find_element_by_xpath('//em[@class="js_joinNum"][1]/text()')
print(aa)
# ss = driver.page_source

# print("=========>", ss.replcae("<!DOCTYPE html>","").replace())
driver.close()
# str1 = "http://news.ifeng.com/a/20190102/60221678_0.shtml?_CPB_404_R7"
#
# s1 = "a"
# s2 = "b"
# s3 = ""
# s3 += s1 + ";" + s2
# print(s3)
# # print(str)
#
# # def strUrl(str1):
# #     str2 = str1.split("/")[4]
# #     return str2
# #
# #
# # str2 = strUrl(str1)
# # print(str2)
