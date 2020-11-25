# coding:utf8
import random

class RandomProxyMiddleware(object):
    def __init__(self):
        self.proxy = self.proxy_generator()

    def proxy_generator(self): 

        username = 'lum-customer-jamalex-zone-static-route_err-pass_dyn'
        password = 'la3ih9r28h2n'
        port = 22225
        session_id = random.random()
        proxy = 'http://{}-session-{}:{}@zproxy.lum-superproxy.io:{}'.format(username, session_id, password, port) 
        
        return proxy

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxy

    def process_exception(self, request, exception, spider):
        request.meta['proxy'] = self.proxy