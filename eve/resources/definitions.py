# coding:utf8
import sys
path = '/'.join(__file__.split('/')[:-2])
sys.path.insert(1, path +'/scripts')
from scripts import generate_spider_setting

tokopedia_search_query = """query SearchProductQuery($params: String) 
                            {
                                CategoryProducts: searchProduct(params: $params) 
                                {
                                    count
                                    data: products 
                                        {
                                            id
                                            url
                                            imageUrl: image_url
                                            imageUrlLarge: image_url_700
                                            catId: category_id
                                            gaKey: ga_key
                                            discountPercentage: discount_percentage
                                            name
                                            price
                                            original_price
                                            shop {
                                                    id
                                                    url
                                                    name
                                                }
                                        }
                                }
                            }"""

tokopedia_search_payload = {'operationName':'SearchProductQuery',
                            'variables':{'params':'&ob=&identifier=&sc={}&user_id=0&rows={}&start={}&source=directory&device=desktop&page={}&related=true&st=product&safe_search=false'},
                            'query': tokopedia_search_query}  
TOKOPEDIA = {
            'allowed_domains': ['{}'],
            'start_urls': ['http://{}/'],
            'custom_settings': {
                                'CONCURRENT_REQUESTS': 15,
                                'DOWNLOAD_TIMEOUT': 30,
                               },
            'headers': {'referer': 'https://www.{}/'},
            'category':{
                       'method': 'POST',
                       'query': tokopedia_search_query,
                       'payload': tokopedia_search_payload,
                       'table': 'tokopedia_cate_info_v1'
                      },
            'venture': '{}',
            'db': '{}',
            'schema': 'raw_data',
            'table': 'worker_failed_info'
            }

LAZADA = {
            'allowed_domains': ['{}'],
            'start_urls': ['https://{}/'],
            'custom_settings': {
                                'CONCURRENT_REQUESTS': 15,
                                'DOWNLOAD_TIMEOUT': 30,
                                'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69',
                                'DOWNLOADER_MIDDLEWARES': {
                                'eve.middlewares.cookie.RemoveCookieMiddleware': 690,
                                'eve.middlewares.proxy.RandomProxyMiddleware': 760
                                                          }
                               },
            'headers': {'referer': '{}/'},
            'category':{
                       'method': 'GET',
                       'table': 'lazada_cate_info_v1'
                      },
            'venture': '{}',
            'db': '{}',
            'schema': 'raw_data',
            'table': 'worker_failed_info'
            }

SHOPEE =    {
            'allowed_domains': ['{}'],
            'start_urls': ['https://{}/'],
            'custom_settings': {
                                'CONCURRENT_REQUESTS': 15,
                                'DOWNLOAD_TIMEOUT': 30,
                               },
            'headers': {'referer': 'https://{}/',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
                        },
            'category':{
                       'method': 'GET',
                       'table': 'shopee_cate_info_product_list_v1'
                      },
            'venture': '{}',
            'db': '{}',
            'schema': 'raw_data',
            'error': 'worker_failed_info' 
            }

SETTING_MAPPING =   {
                    'tokopedia': TOKOPEDIA,
                    'lazada': LAZADA,
                    'shopee': SHOPEE
                    }

PROJECT =   {
            'xmi': {
                    'db': 'xmi',
                    'tokopedia': 'tokopedia.com',
                    'lazada': 'lazada.co.id',
                    'shopee': 'shopee.co.id',
                    }
            }

SPIDER_SETTING = {project: {
                            site: generate_spider_setting(
                                                          SETTING_MAPPING[site], 
                                                          PROJECT[project], 
                                                          site
                                                         ) for site in SETTING_MAPPING.keys() if site != 'db'
                            } for project in PROJECT.keys()
                 }