# coding:utf8

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
            'allowed_domains': ['tokopedia.com'],
            'start_urls': ['http://tokopedia.com/'],
            'custom_settings': {
                                'CONCURRENT_REQUESTS': 15,
                                'DOWNLOAD_TIMEOUT': 30,
                               },
            'headers': {'referer': 'https://www.tokopedia.com/'},
            'category':{
                       'url': 'https://gql.tokopedia.com/',
                       'method': 'POST',
                       'query': tokopedia_search_query,
                       'payload': tokopedia_search_payload,
                       'table': 'tokopedia_cate_info'
                      },
            'venture': 'id',
            'platform': 'tokopedia',
            'db': 'xmi',
            'schema': 'raw_data',
            'table': 'worker_failed_info'
            }

LAZADA = {
            'allowed_domains': ['lazada.co.id'],
            'start_urls': ['https://lazada.co.id/'],
            'custom_settings': {
                                'CONCURRENT_REQUESTS': 15,
                                'DOWNLOAD_TIMEOUT': 30,
                                'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69',
                                'DOWNLOADER_MIDDLEWARES': {
                                'scrappy.middlewares.cookie.RemoveCookieMiddleware': 690,
                                'scrappy.middlewares.proxy.RandomProxyMiddleware': 760
                                                          }
                               },
            'headers': {'referer': 'http://lazada.co.id/'},
            'category':{
                       'method': 'GET',
                       'table': 'lazada_cate_info'
                      },
            'venture': 'id',
            'platform': 'lazada',
            'db': 'xmi',
            'schema': 'raw_data',
            'table': 'worker_failed_info'
            }

SHOPEE = {
            'allowed_domains': ['shopee.co.id'],
            'start_urls': ['https://shopee.co.id/'],
            'custom_settings': {
                                'CONCURRENT_REQUESTS': 15,
                                'DOWNLOAD_TIMEOUT': 30,
                               },
            'headers': {'referer': 'https://shopee.co.id/',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
                        },
            'category':{
                       'method': 'GET',
                       'table': 'shopee_cate_info_product_list'
                      },
            'venture': 'id',
            'platform': 'shopee',
            'db': 'xmi',
            'schema': 'raw_data',
            'error': 'worker_failed_info' 
            }

SPIDER_SETTING = {
                  'tokopedia': TOKOPEDIA,
                  'lazada': LAZADA,
                  'shopee': SHOPEE
                 }