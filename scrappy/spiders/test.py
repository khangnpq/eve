# coding:utf8
__author__ = 'modm'
from scrapy import Request
from scrapy.spiders import CrawlSpider


class TestSpider(CrawlSpider):
    # spider name
    name = 'test'
    # custom settins will overwrite default settings
    custom_settings = {
        'CONCURRENT_REQUESTS': 15,
        'DOWNLOAD_TIMEOUT': 30,
    }

    def __init__(self, category=None, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request('https://github.com/', dont_filter=True)

    def parse(self, response):
        print response.xpath('//title/text()').extract_first()
