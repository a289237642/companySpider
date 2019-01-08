# -*- coding: utf-8 -*-

# Scrapy settings for MapSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'MapSpider'

SPIDER_MODULES = ['MapSpider.spiders']
NEWSPIDER_MODULE = 'MapSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'MapSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 12

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
    #'ser-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
     #'Cookie': '__jsluid=c73c4bae163643ae9a0341c64f22d4f7; global_cookie=bzk2pbwf54omc4vod6pq3rytk1vjlnbpdoq; city=www; Integrateactivity=notincludemc; sfut=9C9EB95A5C73EF52A34EEB3A73D353906500153D2190CAD679102AA0D4AF378146A89A0C258ACBDDF069F5F06BBF7F42541D291ABAFAD634F2932FE3C512D6F05FED27D32B13D073DC14EC6516A722A823394F5AB7A1177FEE4EFF8A7997367E; sf_source=; HomeIdeabook=HomeIdeabook_dealerid=0&HomeIdeabook_usertype=1; JSESSIONID=aaaNEYKxspqI44dgi9axw; Captcha=4431577074436B64496C64425237335A4F5763493635746A51642B5473436F4C434B3174336F3546305167377964647A4E7476776E67696D476864755A427063763446477A2F56396A38593D; new_loginid=108095844; login_username=passport3796374902; s=; showAdquanguo=1; homealbumsearchurl=&limit=36&cityname=%b1%b1%be%a9&searchtype=1&sortid=24&cityname=%b1%b1%be%a9&searchall=1&orsearch=1&isnewvalid=1|1|42213|36; homealbuminfosearchurl=&limit=36&cityname=%b1%b1%be%a9&searchtype=1&sortid=24&cityname=%b1%b1%be%a9&searchall=1&orsearch=1&isnewvalid=1|1|42213|36; unique_cookie=U_t6itrdxtb08fi9dw0gkwki34k15jlt97qkk*73',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
    #'MapSpider.middlewares.MapspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
    #配置随机的浏览器和代理
    #'MapSpider.middlewares.RandomUserAgentMiddleware': 500,
    #把系统的默认关闭掉（否则不起作用）
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'MapSpider.pipelines.MapSpiderImagePipeline': 200,
    #'MapSpider.pipelines.CrawlfangPipeline': 250,
    'MapSpider.pipelines.MapSpiderPipeline': 320,
}

# 配置图片的保存路径
IMAGES_STORE = "./Images"
# 配置日志
# LOG_FILE = "MapSpider.log"
# LOG_LEVEL = "DEBUG"


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False
# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
