# coding:utf8
__author__ = 'modm'
class RemoveCookieMiddleware(object):
    def process_request(self, request, spider):
        request.cookies = {}
        request.headers['cookies'] = ''

    def process_exception(self, request, exception, spider):
        request.cookies = {}
        request.headers['cookies'] = ''