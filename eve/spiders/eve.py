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
import time

class EveSpider(scrapy.Spider):
    # spider name
    name = 'eve'
    url_list = []
    block_flag = False 
    curr = 0
    proxy = proxy_generator()
    proxy_usage = 0

    def __init__(self, category='', *args, **kwargs):
        super(EveSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
    
        if os.path.exists(str(os.getcwd()) + "/../test.txt"):
            self.block_flag = True
            raise scrapy.exceptions.CloseSpider("Current Job not Done yet.")
        else: 
            file = open(str(os.getcwd()) + "/../test.txt", "w+")
            file.close() 
        # worker_manager="http://13.212.181.246:5000/getdata?project=eve_q&num=100"
        if '&num=' in self.worker_manager: # defined number of queue to crawl
            resp = requests.get(self.worker_manager) # proceed to crawl with the exact queues
            data = json.loads(resp.text) 
            self.url_list.extend(data["urls"])
        else: # execute all queue exist in the link
            while True:
                # link = self.worker_manager+ '&num=100'
                resp = requests.get(self.worker_manager + '&num=100')
                data = json.loads(resp.text)
                if data['urls']:
                    self.url_list.extend(data["urls"])
                else:
                    break

        # self.url_list = [ 
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
        # 'shop_id': 148045025,
        # 'project': 'xmi',
        # 'get_review': False 
        # },
        # SHOPEE SELLER
        # {
        # 'url': 'https://shopee.vn/api/v2/shop/get?shopid={}'.format(343663098),
        # 'url_type': 'shopee_shop',
        # 'shop_id': 343663098,
        # 'project': 'DS-3',
        # 'venture': 'vn'
        # },
        # SHOPEE CATEGORY 
        # {
        # "url": 'https://shopee.vn/api/v2/search_items/?by=relevancy&keyword=&limit=50&match_id=2365&newest=0&order=desc&page_type=search&version=2',
        # "url_type": 'shopee_category',
        # "cat_id": 2365, 
        # 'keyword': '',
        # "page": 1, 
        # "project": 'DS-3',
        # 'venture': 'vn'
        # },
        # ]
        
        if find_in_obj(self.url_list, 'shopee_category'):
            self.req = len(self.url_list) + 2
        else:
            self.req = len(self.url_list)
        while True:
            try:
                url = self.url_list.pop(0)
                if url.get('url_type') == 'shopee_category':
                    if self.proxy_usage % 5 == 0 and self.proxy_usage > 0:
                        self.proxy = proxy_generator()
                    self.proxy_usage += 1
                self.curr += 1
            except IndexError:
                if self.curr <= self.req:
                    time.sleep(1)
                else:
                    break
            request, spider_setting = generate_request_arguments(
                                                                url,
                                                                SPIDER_SETTING, 
                                                                self.proxy,
                                                                self.parse_page,
                                                                self.errback_parse
                                                                )
            self.allowed_domains = spider_setting['allowed_domains']
            self.start_urls = spider_setting['start_urls']
            self.custom_settings = spider_setting.get('custom_settings', '')
            yield scrapy.Request(**request)

    def parse_page(self,response):
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
        elif response.meta.get('worker_type') == 'category' or response.meta.get('worker_type') == 'search':
            products_data['cat_id'] = response.meta.get('cat_id')
            products_data['page'] = response.meta.get('page')
            products_data['keyword'] = response.meta.get('keyword')
            # Added crawling shop info task
            shop_list = find_in_obj(json.loads(data), 'shopid')
            for shop_id in shop_list: 
                shop_request = {
                                'url': 'https://shopee.{}/api/v2/shop/get?shopid={}'.\
                                                                    format(
                                                                           response.meta.get('venture'),
                                                                           shop_id, 
                                                                          ),
                                'url_type': 'shopee_shop',
                                'shop_id': shop_id,
                                'project': response.meta.get('project'),
                                'venture': response.meta.get('venture'),
                                }
                shop_lop_request = {
                                'url': 'https://shopee.{}/api/v4/search/search_facet?match_id={}&page_type=shop'.\
                                                                    format(
                                                                           response.meta.get('venture'),
                                                                           shop_id,
                                                                           ),
                                'url_type': 'shopee_shop_lop',
                                'shop_id': shop_id,
                                'project': response.meta.get('project'),
                                'venture': response.meta.get('venture'),
                                }
                self.url_list.append(shop_request)
                self.url_list.append(shop_lop_request)
            yield products_data 
        
        elif response.meta.get('worker_type') == 'shop' or response.meta.get('worker_type') == 'shop_lop':
            products_data['shop_id'] = response.meta.get('shop_id')
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
            self.logger.warning('Proxy usage: %s', self.proxy_usage)