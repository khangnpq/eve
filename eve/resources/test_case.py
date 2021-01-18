REQUEST_LIST = [ 
            # TOKOPEDIA CATEGORY
            # {
            # "url": "https://gql.tokopedia.com/",
            # "url_type": "tokopedia_category",
            # "sc": 24,
            # "row": 60,
            # "page": 1,
            # "project": "xmi"
            # },
            # TOKOPEDIA SEARCH
            # {
            # "url": "https://gql.tokopedia.com/",
            # "url_type": "tokopedia_search",
            # "keyword": "xiaomi",
            # "row": 60,
            # "page": 1,
            # "project": "xmi"
            # },
            # LAZADA SELLER CENTER
            # {
            # "url": "https://www.lazada.co.id/shop/site/api/seller/products?shopId=8234&offset=0&limit=50",
            # "url_type": "lazada_seller_center",
            # "shop_id": 8234, 
            # "project": "xmi"
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
            {
            "url": "https://shopee.vn/api/v2/item/get?itemid={}&shopid={}".format(1819126512, 69839196), 
            "request_type": "shopee_product",
            "platform": "shopee",
            "venture": "vn",
            "database": "eve",
            "schema": "DS-3_raw_data",
            "item_id": 1819126512,
            "shop_id": 69839196,
            "get_review": 'false',
            "use_proxy": False
            },
            # {
            # "url": "https://shopee.vn/api/v2/item/get?itemid={}&shopid={}".format(3517890333, 69839196), 
            # "url_type": "shopee_product",
            # "item_id": 3517890333,
            # "shop_id": 69839196,
            # "project": "DS-3",
            # "get_review": False 
            # },
            # {
            # "url": "https://shopee.vn/api/v2/item/get?itemid={}&shopid={}".format(6439237117, 69839196), 
            # "url_type": "shopee_product",
            # "item_id": 6439237117,
            # "shop_id": 69839196,
            # "project": "DS-3",
            # "get_review": False 
            # },
            # {
            # "url": "https://shopee.vn/api/v2/item/get?itemid={}&shopid={}".format(7400114527, 69839196), 
            # "url_type": "shopee_product",
            # "item_id": 7400114527,
            # "shop_id": 69839196,
            # "project": "DS-3",
            # "get_review": False 
            # },
            # {
            # "url": "https://shopee.vn/api/v2/item/get?itemid={}&shopid={}".format(5941797573, 69839196), 
            # "url_type": "shopee_product",
            # "item_id": 5941797573,
            # "shop_id": 69839196,
            # "project": "DS-3",
            # "get_review": False 
            # },
            # SHOPEE SELLER
            # {
            # "url": "https://shopee.vn/api/v2/shop/get?shopid={}".format(343663098),
            # "url_type": "shopee_shop",
            # "shop_id": 343663098,
            # "project": "DS-3",
            # "venture": "vn"
            # },
            # SHOPEE CATEGORY 
            # {
            # "url": "https://shopee.vn/api/v2/search_items/?by=relevancy&keyword=&limit=50&match_id=2365&newest=0&order=desc&page_type=search&version=2",
            # "url_type": "shopee_category",
            # "cat_id": 2365, 
            # "keyword": "",
            # "page": 1, 
            # "project": "DS-3",
            # "venture": "vn"
            # },
            ]