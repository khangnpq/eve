BOT_NAME = 'github.com/dormymo/scrappy'
SPIDER_MODULES = ['scrappy.spiders']
NEWSPIDER_MODULE = 'scrappy.spiders'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 408]
RETRY_TIMES = 20
# DOWNLOAD_DELAY=0.25
DOWNLOAD_TIMEOUT = 60
CONCURRENT_REQUESTS = 16
CONCURRENT_ITEMS = 100
# CONCURRENT_REQUESTS_PER_DOMAIN=1
# CONCURRENT_REQUESTS_PER_IP=1
REACTOR_THREADPOOL_MAXSIZE = 10
# COOKIES_ENABLED=False
# TELNETCONSOLE_ENABLED=False
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
    'Connection': 'keep-alive'
}
'''
Default :
{
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}

'''

DOWNLOADER_MIDDLEWARES = {
    # 'scrappy.middlewares.cookie.RemoveCookieMiddleware': 690,
    # 'scrappy.middlewares.proxy.RandomProxyMiddleware': 760,
    'scrappy.middlewares.useragent.UserAgentMiddleware': 390,

}
EXTENSIONS = {
    'scrapy.telnet.TelnetConsole': None,
    'scrapy.extensions.feedexport.FeedExporter': None,
    'scrappy.extensions.scrapy_jsonrpc.webservice.WebService': 100
}
ITEM_PIPELINES = {
    'scrappy.pipelines.ScrappyPipeline': 300
}
AUTOTHROTTLE_ENABLED = False
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_DELAY = 0
AUTOTHROTTLE_MAX_DELAY = 40
AUTOTHROTTLE_DEBUG = False

# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

'''
extensions
'''
##redis
##redis
ENABLE_REDIS = False
if ENABLE_REDIS:
    SCHEDULER = "scrappy.extensions.scrapy_redis.scheduler.Scheduler"
    # Don't cleanup redis queues, allows to pause/resume crawls.
    SCHEDULER_PERSIST = True
    # Schedule requests using a priority queue. (default)
    SCHEDULER_QUEUE_CLASS = 'scrappy.extensions.scrapy_redis.queue.SpiderPriorityQueue'
    # # Max idle time to prevent the spider from being closed when distributed crawling.
    # This only works if queue class is SpiderQueue or SpiderStack,
    # and may also block the same time when your spider start at the first time (because the queue is empty).
    SCHEDULER_IDLE_BEFORE_CLOSE = 10
    ##stats
    STATS_CLASS = 'scrappy.extensions.stat.statcollection.RedisStatsCollector'

JSONRPC_ENABLED = True
JSONRPC_PORT = None

'''
custom settings
'''
LOG_LEVEL = 'DEBUG'

REDIS_URL = 'redis://localhost:6379'
JSONRPC_HOST = 'localhost'
# resource absolute direction
RESOURCE_DIR = "/Users/modm/github/scrappy/scrappy/resources"
# MYSQl
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'
MYSQL_DB = 'test'
# Mongo
MONGO_URL = 'mongodb://user:password@localhost/db_name?authMechanism=SCRAM-SHA-1'
