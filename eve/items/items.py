# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class Template(scrapy.Item):

    database = scrapy.Field()
    schema = scrapy.Field()
    created_at = scrapy.Field()
    venture = scrapy.Field()
    platform = scrapy.Field()
    table = scrapy.Field()
    data = scrapy.Field()
    data_key = scrapy.Field()
    
class Products(Template):

    is_cleaned = scrapy.Field()
    
    def handleInsert(self, item, column_list):
        info = {}
        for key, val in item.items():
            # if key not in ['depth', 'download_latency', 'download_slot', 'download_timeout',
            #                'database', 'schema', 'table']:
            if key in column_list:
                info[key] = val
        return info

    # def handleUpdate(self, item):
    #     return item

class ErrorInfo(Template):

    def handleInsert(self, item, column_list):
        info = {}
        for key, val in item.items():
            # if key not in ['depth', 'download_latency', 'download_slot', 'download_timeout',
            #                'database', 'schema', 'table']:
            if key in column_list:
                info[key] = val
        return info
