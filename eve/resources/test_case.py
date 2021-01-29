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
            # {
            # "url": "https://shopee.vn/api/v2/item/get?itemid={}&shopid={}".format(1819126512, 69839196), 
            # "request_type": "shopee_product",
            # "platform": "shopee",
            # "venture": "vn",
            # "database": "eve",
            # "schema": "DS-3_raw_data",
            # "item_id": 1819126512,
            # "shop_id": 69839196,
            # "get_review": 'false',
            # "use_proxy": False
            # },
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

            # TIKI PRODUCT PAGE
            {
            "url": "https://tiki.vn/thung-48-hop-sua-tuoi-tiet-trung-dutch-lady-co-gai-ha-lan-co-duong-48x180ml-p2454283.html?spid=2599793&src=ss-organic",
            "request_type": "tiki_product",
            "platform": "tiki",
            "venture": "vn",
            "database": "fcv",
            "schema": "raw_data",
            "table": "tiki_product_info_v1",
            "use_proxy": False,
            "keep_url": True
            },

            # TIKI PRODUCT REVIEWS
            # {
            # "url": "https://tiki.vn/api/v2/reviews?product_id=2454283&sort=bought&page=1&limit=10&include=comments",
            # "request_type": "tiki_product_review",
            # "platform": "tiki",
            # "venture": "vn",
            # "database": "fcv",
            # "schema": "raw_data",
            # "table": "tiki_product_review",
            # "use_proxy": False,
            # },

            # TIKI PRODUCT COUPONS
            # {
            # "url": "https://api.tiki.vn/shopping/v2/promotion/rules?pid=2599793&seller_id=1",
            # "request_type": "tiki_product_coupon",
            # "platform": "tiki",
            # "venture": "vn",
            # "database": "fcv",
            # "schema": "raw_data",
            # "table": "tiki_product_coupon",
            # "use_proxy": False,
            # },

            # TIKI SEARCH
            # {
            # "url": "https://tiki.vn/api/v2/products?limit=48&q=sữa&page=1",
            # "request_type": "tiki_search",
            # "platform": "tiki",
            # "venture": "vn",
            # "database": "eve",
            # "schema": "DS-3_raw_data",
            # "page": 1,
            # "keyword": "sữa",
            # "use_proxy": False
            # }

            # TIKI CATEGORY
            # {
            # "url": "https://tiki.vn/do-choi-me-be/c2549?src=mega-menu?page=1",
            # "request_type": "tiki_category",
            # "platform": "tiki",
            # "venture": "vn",
            # "database": "eve",
            # "schema": "DS-3_raw_data",
            # "page": 1,
            # "use_proxy": False
            # }

            # TIKI BRAND SEARCH 
            # {
            # "url": "https://tiki.vn/search?q=dutch+lady&category=8273&brand=32546&seller=1&page=1",
            # "request_type": "tiki_brand_search",
            # "platform": "tiki",
            # "venture": "vn",
            # "database": "fcv",
            # "schema": "raw_data",
            # "table": "tiki_brand_search",
            # "brand_name": "Dutch Lady",
            # "page": 1,
            # "use_proxy": False
            # }   

            # TIKI BRAND PAGE
            # {
            # "url": "https://tiki.vn/chuong-trinh/enfa-chinh-hang",
            # "request_type": "tiki_brand_page",
            # "platform": "tiki",
            # "venture": "vn",
            # "database": "eve",
            # "schema": "DS-3_raw_data",
            # "page": 1,
            # "use_proxy": False
            # }

            # TIKI BRAND PAGE LV2
            # {
            # "url": "https://tiki.vn/api/v2/landingpage/products?skus=8936036773798",
            # "url_type": "tiki_brand_page_lv2" 
            # }

            # TIKI FLASH SALE 
            # {
            # "url": "https://tiki.vn/api/v2/widget/deals/mix?type=now&page=1&per_page=20",
            # "url_type": "tiki_flash_sale",
            # "page": 1 
            # }

            # TIKI CAMPAIGN
            # {
            # "url": "https://tiki.vn/chuong-trinh/me-san-khuyen-mai-online?src=home_v4_main_banner.s3.b41521",
            # "url_type": "tiki_campaign"
            # }
]