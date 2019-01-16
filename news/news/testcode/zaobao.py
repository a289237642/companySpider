#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urlparse, urlsplit

mapping = {
    'realtime.china': '即时报道;中港台即时',
    'realtime.world': '即时报道;国际即时',
    'news.china': '新闻;中国新闻',
    'news.world': '新闻;国际新闻'
}

# mapping2 = {
#     'realtime': {
#         'china': '中港台即时',
#         'world': '国际即时'
#     },
#     'news': {
#         'china': '中国新闻',
#         'world': '国际新闻'
#     }
#
# }


url = 'http://www.zaobao.com/realtime/china/story20190105-921429'
o = urlparse(url)
print(o.path)
print(o.path.strip('/').split('/'))
