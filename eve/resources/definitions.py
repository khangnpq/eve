# coding:utf8
import sys
path = '/'.join(__file__.split('/')[:-2])
sys.path.insert(1, path +'/scripts')
from scripts import generate_spider_setting

tokopedia_search_query = """query SearchProductQueryV4($params: String!) {    ace_search_product_v4(params: $params) {      header {        totalData        totalDataText        processTime        responseCode        errorMessage        additionalParams        keywordProcess        __typename      }      data {        isQuerySafe        ticker {          text          query          typeId          __typename        }        redirection {          redirectUrl          departmentId          __typename        }        related {          relatedKeyword          otherRelated {            keyword            url            product {              id              name              price              imageUrl              rating              countReview              url              priceStr              wishlist              shop {                city                isOfficial                isPowerBadge                __typename              }              ads {                id                productClickUrl                productWishlistUrl                shopClickUrl                productViewUrl                __typename              }              __typename            }            __typename          }          __typename        }        suggestion {          currentKeyword          suggestion          suggestionCount          instead          insteadCount          query          text          __typename        }        products {          id          name          ads {            id            productClickUrl            productWishlistUrl            productViewUrl            __typename          }          badges {            title            imageUrl            show            __typename          }          category: departmentId          categoryBreadcrumb          categoryId          categoryName          countReview          discountPercentage          gaKey          imageUrl          labelGroups {            position            title            type            __typename          }          originalPrice          price          priceRange          rating          shop {            id            name            url            city            isOfficial            isPowerBadge            __typename          }          url          wishlist          sourceEngine: source_engine          __typename        }        __typename      }      __typename    }  } """
tokopedia_category_query = """query SearchProductQuery($params: String) 
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

tokopedia_category_payload = {'operationName':'SearchProductQuery',
                            'variables':{'params':'&ob=&identifier=&sc={}&user_id=0&rows={}&start={}&source=directory&device=desktop&page={}&related=true&st=product&safe_search=false'},
                            'query': tokopedia_category_query}

tokopedia_search_payload = {'operationName':'SearchProductQueryV4',
                            'variables':{'params':'device=desktop&ob=&page={}&q={}&related=true&rows={}&shipping=&source=search&st=product&start={}&unique_id=&user_id=&variants='},
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
                       'query': tokopedia_category_query,
                       'payload': tokopedia_category_payload,
                       'table': 'tokopedia_cate_info_v1'
                      },
            'search':{
                       'method': 'POST',
                       'query': tokopedia_search_query,
                       'payload': tokopedia_search_payload,
                       'table': 'tokopedia_search_info_v1'
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
            'product':{
                       'method': 'GET',
                       'table': 'lazada_product_info'
                      },
            'seller_center':{
                       'method': 'GET',
                       'table': 'lazada_seller_center'
                      },
            'category':{
                       'method': 'GET',
                       'table': 'lazada_cate_info_v1'
                      },
            'search':  {
                        'method': 'GET',
                        'table': 'lazada_search_info'},
            'venture': '{}',
            'db': '{}',
            'schema': 'raw_data',
            'table': 'worker_failed_info'
            }

SHOPEE =    {
            'allowed_domains': ['{}'],
            'start_urls': ['https://{}/'],
            'custom_settings': {
                                'CONCURRENT_REQUESTS': 50,
                                'DOWNLOAD_TIMEOUT': 30,
                                'DOWNLOADER_MIDDLEWARES': {
                                'eve.middlewares.cookie.RemoveCookieMiddleware': 40,
                                # 'eve.middlewares.proxy.RandomProxyMiddleware': 30}
                                }
                               },
            'headers': {'referer': 'https://{}/',
                        # 'if-none-match-': '55b03-0b65cbc01e512d9bf12c34f1f8deeedb',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
                        },
            'product': {
                        'method': 'GET',
                        'table': 'lazada_product_info'
                        },
            'category': {
                        'method': 'GET',
                        'table': 'shopee_category'
                        },
            'shop': {
                    'method': 'GET',
                    'table': 'shopee_shop'
                    },
            'shop_lop': {
                    'method': 'GET',
                    'table': 'shopee_shop_lop'
                    },
            'venture': '{}',
            'db': 'eve',
            'schema': 'DS-3_raw_data',
            'error': 'worker_failed_info' 
            }

SETTING_MAPPING =   {
                    'tokopedia': TOKOPEDIA,
                    'lazada': LAZADA,
                    'shopee': SHOPEE
                    }

PROJECT =   {
            'DS-3': {
                    'db': 'eve',
                    'tokopedia': 'tokopedia.com',
                    'lazada': 'lazada.co.id',
                    'shopee': 'shopee.vn',
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