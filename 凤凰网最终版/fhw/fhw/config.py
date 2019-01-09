#!/usr/bin/env python3

import os

from selenium.webdriver.chrome.options import Options


BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
windows_chrome_driver = os.path.join(BASEDIR, 'drivers', 'chromedriver.exe')
linux_chrome_driver = os.path.join(BASEDIR, 'drivers', 'chromedriver')

# print(BASEDIR)
# print(windows_chrome_driver)
# print(linux_chrome_driver)


def get_chrome_options():
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return chrome_options
