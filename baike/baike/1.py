from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://baike.baidu.com/item/%E8%81%94%E5%90%88%E5%9B%BD/135426"


def handlejs(url):
    # item = FhwItem()
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    MC = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[2]/dl[1]/dd/h1").text
    YWMC=driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[2]/div[7]/dl[1]/dd[2]").text

    #  YWMC   #QTMC  BKLY GXSJ CJSJ RKSJ FLLJ YS_URL CL_URL TP_URL
    return s


a1 = handlejs(url)
print(a1)
