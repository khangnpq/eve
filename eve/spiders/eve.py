# coding:utf8
import scrapy
import requests
import json
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from eve.scripts.scripts import generate_request_arguments, generate_item_class
from eve.resources.definitions import SPIDER_SETTING

class EveSpider(scrapy.Spider):
    name = 'eve'

    def __init__(self, worker_manager=None, request_list=None, *args, **kwargs):
        super(EveSpider, self).__init__(*args, **kwargs)
        if worker_manager:
            self.worker_manager = worker_manager

    def start_requests(self):
        if hasattr(self, 'worker_manager'): # not a test case
            # worker_manager = "http://13.212.181.246:5000/getdata?project=fcv_l&num=100"
            data = requests.get(self.worker_manager)
            data = json.loads(data.text) 
            self.request_list = data.get("urls")
        else: # reources/test_case.py
            from eve.resources.test_case import REQUEST_LIST
            self.request_list = REQUEST_LIST
        if not self.request_list: 
            raise scrapy.exceptions.CloseSpider("No Job.")
        for request_meta in self.request_list:
            request = generate_request_arguments(
                                                 request_meta=request_meta,
                                                 SETTING=SPIDER_SETTING, 
                                                 parse_page=self.parse_page,
                                                 err_parse=self.errback_parse
                                                )
            yield scrapy.Request(**request)

    def parse_page(self, response):
        data = response.text 
        products_data = generate_item_class(
                                            name=response.meta.get('table'),
                                            field_list=response.meta.keys(),
                                            template='product'
                                           )
        products_data['data'] = data
        for key, val in response.meta.items():
            products_data[key] = val
        yield products_data
    
    def errback_parse(self, failure):
        # this is the original request
        request = failure.request
        failed_url = request.url
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            failed_reason = 'HttpError'
            self.logger.error('HttpError on %s', failed_url)
        elif failure.check(DNSLookupError):
            failed_reason = 'DNSLookupError'
            self.logger.error('DNSLookupError on %s', failed_url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            failed_reason = 'TimeoutError'
            self.logger.error('TimeoutError on %s', failed_url)
        else:
            failed_reason = repr(failure)
        error_data = generate_item_class(
                                         name=failure.request.meta.get('table'), 
                                         field_list=['request_meta', 'failed_reason'], 
                                         template='error'
                                        )
        request_meta = {}
        for key, val in failure.request.meta.items():
            if key not in ['proxy', 'download_timeout', 'download_slot']:
                request_meta[key] = val
            elif key == 'proxy':
                request_meta['proxy'] = True
        request_meta['url'] = failed_url
        if 'proxy' not in request_meta:
            request_meta['proxy'] = False
        error_data['request_meta'] = request_meta
        error_data['failed_reason'] = failed_reason
        error_data['table'] = 'worker_failed_info'
        error_data['database'] = request_meta['database']
        error_data['schema'] = request_meta['schema']
        yield error_data              

    def close(self, reason):  
        # if not self.block_flag:
        #     pass
        #     os.remove(str(os.getcwd()) + "/../test.txt")
        self.logger.warning('Spider finished successfully!')
