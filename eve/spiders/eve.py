# coding:utf8
import scrapy
import json
import random
from datetime import datetime
from eve.items.items import Products, ErrorInfo, generate_item_class
from eve.scripts.scripts import *
from eve.resources.definitions import * 
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class EveSpider(scrapy.Spider):
    # spider name
    name = 'eve'
    def __init__(self, category=None, *args, **kwargs):
        super(EveSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        
        if os.path.exists(str(os.getcwd()) + "/../test.txt"):
            self.block_flag = True
            raise scrapy.exceptions.CloseSpider("Current Job not Done yet.")
        else: 
            file = open(str(os.getcwd()) + "/../test.txt", "w+")
            file.close() 
        worker_manager = "http://13.212.181.246:5000/getdata?project=fcv_q&num=100"
        worker_manager_low = "http://13.212.181.246:5000/getdata?project=xmi_ql&num=100"

        # data = requests.get(worker_manager)
        # data = json.loads(data.text) 
        # urls_list = data["urls"]

        if len(urls_list) == 0: 
            data_low = requests.get(worker_manager_low)
            data_low = json.loads(data_low.text) 
            urls_list = data_low["urls"]

        if len(urls_list) == 0: 
            raise scrapy.exceptions.CloseSpider("No Job.")

        # urls_list = [   
                    # TOKOPEDIA CATEGORY
                    # {
                    # "url": 'https://gql.tokopedia.com/',
                    # "url_type": "tokopedia_category",
                    # 'sc': 65,
                    # 'row': 60,
                    # 'page': 1,
                    # 'project': 'xmi'
                    # },
                    # LAZADA CATEGORY PAGE 
                    # {
                    # "url": "https://www.lazada.co.id/beli-handphone/?page=1",
                    # "url_type": "lazada_category",
                    # "page": 1,
                    # "venture": "id",
                    # "project": "xmi"
                    # },
                    # SHOPEE CATEGORY PAGE 
                    # {
                    # "url": 'https://shopee.co.id/api/v2/search_items/?by=relevancy&limit=50&match_id=1211&newest=0&order=desc&page_type=search&version=2',
                    # "url_type": 'shopee_category',
                    # "cat_id": 1211, 
                    # "page": 1, 
                    # "project": 'xmi'
                    # }
                    # ]
        for url in urls_list:
            platform = url.get('url_type').split('_')[0]
            project = url.get('project')
            spider_setting = SPIDER_SETTING[project][platform]

            self.allowed_domains = spider_setting['allowed_domains']
            self.start_urls = spider_setting['start_urls']
            self.custom_settings = spider_setting.get('custom_settings', '')
            request = generate_request_arguments(url, spider_setting, self.parse_page, self.errback_parse)
            
            yield scrapy.Request(*request)

    def parse_page(self,response):
        try:
            data = json.loads(response.text) 
        except:
            data = response.text 

        products_data = generate_item_class(response.meta.get('project') + '_' + response.meta.get('url_type'), template=Products)
        products_data['info'] = data
        if response.meta.get('page'):
            products_data['page'] = response.meta.get('page')
        yield products_data 
    
    def errback_parse(self, failure):

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            failed_url = response.url
            failed_status = 'HttpError'
            self.logger.error('HttpError on %s', failed_url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            failed_url = request.url
            failed_status = 'DNSLookupError'
            self.logger.error('DNSLookupError on %s', failed_url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            failed_url = request.url
            failed_status = 'TimeoutError'
            self.logger.error('TimeoutError on %s', failed_url)
        error_data = generate_item_class(name=response.meta.get('project') + '_' + response.meta.get('url_type'), template=ErrorInfo)
        error_data['failed_url'] = failed_url
        error_data['failed_status'] = failed_status

        yield error_data              
        
    def close(self, reason):  
        if not self.block_flag:
            os.remove(str(os.getcwd()) + "/../test.txt") 
            