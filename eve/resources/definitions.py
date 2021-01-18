# coding:utf8

SPIDER_SETTING = {
                "lazada": {
                            "headers": {
                                        "referer": "https://{}/"
                                      },
                            "product": {
                                        "table": "lazada_product_info"
                                      },
                            "seller_center": {
                                        "table": "lazada_seller_center"
                                      },
                            "category": {
                                        "table": "lazada_cate_info_v1"
                                      },
                            "search": {
                                        "table": "lazada_search_info"
                                      }
                          },
                "shopee": {
                          "headers": {
                                      "referer": "https://{}/"
                                    },
                          "product": {
                                        "table": "shopee_product_info"
                                    },
                          "category": {
                                        "table": "shopee_category"
                                      },
                          "shop": {
                                        "table": "shopee_shop"
                                  },
                          "shop_lop": {
                                        "table": "shopee_shop_lop"
                                      }
                          }
                }