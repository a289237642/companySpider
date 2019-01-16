#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import base64

# from pyquery import PyQuery
# from bs4 import BeautifulSoup
from lxml import etree
import requests

from news.config import BASEDIR


def process_image_src(html, img_xpath):
    html = etree.HTML(html)
    images = html.xpath(img_xpath)

    if images:
        img = images[0]
        img_url = img.get('src')
        img_b64 = image_base64(img_url)
        if img_b64:
            src = 'data:image/jpg;base64,{b64}'.format(b64=img_b64)
            img.set('src', src)
            return etree.tostring(html, encoding='utf-8').decode('utf-8')
        else:
            return html
    else:
        return html


def image_base64(url):
    try:
        r = requests.get(url, timeout=20)
        return base64.b64encode(r.content).decode('utf-8')
    except Exception as e:
        return ''

    # try:
    #     with open(path, 'rb') as f:
    #         return base64.b64encode(f.read()).decode('utf-8')
    # except FileNotFoundError as e:
    #     return ''

# tree = html.getroottree()
if __name__ == '__main__':
    resource_dir = os.path.join(BASEDIR, 'resource')
    html_path = os.path.join(resource_dir, 'test.html')
    img_path = os.path.join(resource_dir, '3c35fed2e5bdf44_size74_w623_h430.jpg')
    # xpath = '//p[@class="detailPic"]/img|//div[@class="yc_con_txt"]/p/img|//div[@id="main_content"]/p/img|//div[@class="box02"][1]/img'
    #
    with open(html_path, 'r') as f:
        html_str = f.read()

    print(process_image_src(html_str, '//img'))

    # image_base64('http://e.hiphotos.baidu.com/image/pic/item/83025aafa40f4bfb0f815ad60e4f78f0f63618db.jpg')

    # with open('222.jpg', 'rb') as f:
    #     f.read()