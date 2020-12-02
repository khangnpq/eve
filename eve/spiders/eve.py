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
import os
import requests

class EveSpider(scrapy.Spider):
    # spider name
    name = 'eve'
    block_flag = False 
    def __init__(self, category=None, *args, **kwargs):
        super(EveSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        
        # if os.path.exists(str(os.getcwd()) + "/../test.txt"):
        #     self.block_flag = True
        #     raise scrapy.exceptions.CloseSpider("Current Job not Done yet.")
        # else: 
        #     file = open(str(os.getcwd()) + "/../test.txt", "w+")
        #     file.close() 
        worker_manager = "http://13.212.181.246:5000/getdata?project=fcv_q&num=100"
        worker_manager_low = "http://13.212.181.246:5000/getdata?project=xmi_ql&num=100"
        urls_list = []
        # data = requests.get(worker_manager)
        # data = json.loads(data.text) 
        # urls_list = data["urls"]

        if len(urls_list) == 0: 
            data_low = requests.get(worker_manager_low)
            data_low = json.loads(data_low.text) 
            urls_list = data_low["urls"]

        # if len(urls_list) == 0: 
        #     raise scrapy.exceptions.CloseSpider("No Job.")
        # for i in range(1,2):
        #     urls_list.append({
        #             "url": 'https://gql.tokopedia.com/',
        #             "url_type": "tokopedia_search",
        #             'keyword': 'redmi 9c',
        #             'row': 60,
        #             'page': i,
        #             'project': 'xmi'
        #             })
        # urls_list = [   
                    # TOKOPEDIA CATEGORY
                    # {
                    # "url": 'https://gql.tokopedia.com/',
                    # "url_type": "tokopedia_category",
                    # 'sc': 24,
                    # 'row': 60,
                    # 'page': 1,
                    # 'project': 'xmi'
                    # },
                    # TOKOPEDIA SEARCH
                    # {
                    # "url": 'https://gql.tokopedia.com/',
                    # "url_type": "tokopedia_search",
                    # 'keyword': 'xiaomi',
                    # 'row': 60,
                    # 'page': 1,
                    # 'project': 'xmi'
                    # },
                    # LAZADA SELLER CENTER
                    # {
                    # "url": 'https://www.lazada.co.id/shop/site/api/seller/products?shopId=8234&offset=0&limit=50',
                    # "url_type": 'lazada_seller_center',
                    # "shop_id": 8234, 
                    # "project": 'xmi'
                    # },
                    # LAZADA CATEGORY 
                    # {
                    # "url": "https://www.lazada.co.id/beli-handphone/?page=1",
                    # "url_type": "lazada_category",
                    # "page": 1,
                    # "project": "xmi"
                    # },
                    # LAZADA SEARCH 
                    # {
                    # "url": "https://www.lazada.co.id/catalog/?q=Anti-Aging&page=1",
                    # "url_type": "lazada_search",
                    # "page": 1,
                    # "keyword": "Anti-Aging",
                    # "project": "xmi"
                    # },
                    # SHOPEE PRODUCT
                    # {
                    # 'url': 'https://shopee.co.id/api/v2/item/get?itemid={}&shopid={}'.format(7424601528, 148045025), 
                    # 'url_type': 'shopee_product',
                    # 'item_id': 7424601528,
                    # 'shope_id': 148045025,
                    # 'project': 'xmi',
                    # 'get_review': False 
                    # },
                    # SHOPEE CATEGORY 
                    # {
                    # "url": 'https://shopee.co.id/api/v2/search_items/?by=relevancy&limit=50&match_id=1211&newest=0&order=desc&page_type=search&version=2',
                    # "url_type": 'shopee_category',
                    # "cat_id": 1211, 
                    # "page": 1, 
                    # "project": 'xmi'
                    # },
                    # },
                    # ]
        for url in urls_list:
            platform = url.get('url_type').split('_')[0]
            project = url.get('project')
            spider_setting = SPIDER_SETTING[project][platform]

            self.allowed_domains = spider_setting['allowed_domains']
            self.start_urls = spider_setting['start_urls']
            self.custom_settings = spider_setting.get('custom_settings', '')
            request = generate_request_arguments(url, spider_setting, self.parse_page, self.errback_parse)
            yield scrapy.Request(**request)

    def parse_page(self,response):
        try:
            data = response.text # escape_dict(json.loads(response.text)) 
        except:
            data = response.text 
        products_data = generate_item_class(response.meta.get('project') + '_' + response.meta.get('platform') + '_' + response.meta.get('worker_type'), template=Products)
        products_data['info'] = data

        if response.meta.get('worker_type') == 'product':        
            if response.meta.get('platform') == 'lazada':
                current_limit = int(response.request.url.split('limit=')[1])
                total_item = json.loads(response.text).get("result").get("total")
                request = response.meta['request']
                if total_item > current_limit: 
                    request['url'] = re.sub("limit=" + str(current_limit), "limit=" + str(total_item), request['url'])
                    yield scrapy.Request(**request)
                else:
                    yield products_data 
            else:
                yield products_data
        elif response.meta.get('worker_type') == 'category':
            products_data['page'] = response.meta.get('page')
            yield products_data 
            # url_path = find_path(data, 'url')
            # request = generate_request_arguments(url, spider_setting, self.parse_page, self.errback_parse)
        elif response.meta.get('worker_type') == 'search':
            products_data['page'] = response.meta.get('page')
            products_data['keyword'] = response.meta.get('keyword')
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
            # os.remove(str(os.getcwd()) + "/../test.txt") 
            pass