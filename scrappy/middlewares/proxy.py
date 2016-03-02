# coding:utf8
__author__ = 'modm'
class RandomProxyMiddleware(object):
    def __init__(self):
        pass

    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:8888"

    def process_exception(self, request, exception, spider):
        request.meta['proxy'] = "http://127.0.0.1:8888"