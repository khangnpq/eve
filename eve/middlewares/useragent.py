# coding:utf8
import random
from eve.resources.helper import ResourceHelper

class UserAgentMiddleware(object):
    def __init__(self):
        self.resourceHelper = ResourceHelper()
        self.user_agent_list = self.resourceHelper.loadJson('useragent.json')
        self.uaCache = {}

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers['User-Agent'] = ua

    def process_exception(self, request, exception, spider):
        ua = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = ua