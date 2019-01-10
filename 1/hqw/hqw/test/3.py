from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# url = "http://news.ifeng.com/a/20190104/60223969_0.shtml"
url = 'http://taiwan.huanqiu.com/article/2018-12/13943256.html'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get(url)

aa = driver.find_element_by_xpath(
    '//span[@id="msgNumBottom"]/a|//b[@id="msgNumTop"]/a|//b[@id="msgNumBottom"]/a|//span[@class="participate"]/var[0]').text
print(aa)
