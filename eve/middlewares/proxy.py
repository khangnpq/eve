# coding:utf8
import os
import random
from configparser import ConfigParser

class RandomProxyMiddleware(object):
    def __init__(self):
        self.proxy = self.proxy_generator()

    def proxy_generator(self): 

        # read config file
        parser = ConfigParser()
        parser.read(os.path.dirname(os.path.realpath(__file__)) + '/../resources/credentials.ini')
        if parser.has_section('proxy'):
            credentials = dict(parser.items('proxy'))
        session_id = random.random()
        proxy = 'http://{}-session-{}:{}@zproxy.lum-superproxy.io:{}'.format(
                                                                             credentials['username'], 
                                                                             session_id, 
                                                                             credentials['password'], 
                                                                             credentials['port']
                                                                            ) 
        
        return proxy

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxy

    def process_exception(self, request, exception, spider):
        request.meta['proxy'] = self.proxy