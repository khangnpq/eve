# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class Template(scrapy.Item):

    db = scrapy.Field()
    schema = scrapy.Field()
    created_at = scrapy.Field()
    venture = scrapy.Field()
    platform = scrapy.Field()

class Products(Template):

    table = scrapy.Field()
    info = scrapy.Field()
    shop_id = scrapy.Field()
    page = scrapy.Field()
    cat_id = scrapy.Field()
    keyword = scrapy.Field()
    # conflict_do_nothing = scrapy.Field()

    def handleInsert(self, item):
        info = {
                'venture': item.get('venture'),
                'platform': item.get('platform'),
                'created_at': item.get('created_at'),
                'data': item.get('info')
                }
        if item.get('page'):
            info['page'] = item.get('page')

        if item.get('cat_id'):
            info['cat_id'] = item.get('cat_id')

        if item.get('keyword'):
            info['keyword'] = item.get('keyword')

        if item.get('shop_id'):
            info['shop_id'] = item.get('shop_id')
            
            
        return info

    # def handleUpdate(self, item):
    #     return item

class ErrorInfo(Template):

    table = scrapy.Field()
    failed_url = scrapy.Field()
    failed_status = scrapy.Field()

    def handleInsert(self, item):
        info = {
                'venture': item.get('venture'),
                'platform': item.get('platform'),
                'created_at': item.get('created_at'),
                'failed_url': item.get('failed_url'),
                'pfailed_statusage': item.get('failed_status')
                }
        return info

def generate_item_class(name, template=Products):
    return type(name,(template,), {})()
