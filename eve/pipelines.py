# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import platform
import logging
from itemadapter import ItemAdapter
from datetime import datetime
from eve.dbs.postgre import PostgreSQLClient
from eve.scripts.scripts import *
from eve.resources.definitions import * 
# class ScrappyPipeline(object):
#     def __init__(self):
#         self.postgreDict = {}
#         self.collection_name_map = {'ScrappyItem': "xmi"}  #model class name to postgreDB collection

#     def _getPostgreInstance(self, item):
#         itemClassName = item.__class__.__name__
#         collection_name = ''
#         for className in self.collection_name_map.keys():
#             if itemClassName == className:
#                 collection_name = self.collection_name_map[itemClassName]
#         if collection_name not in self.postgreDict:
#             self.postgreDict[collection_name] = PostgreSQLClient(collection_name)
#         return self.postgreDict[collection_name]

#     def process_item(self, item, spider):
#         # postgreInstance = self._getPostgreInstance(item)
#         content = ItemAdapter(item)
#         if type(content['info']) == list:
#             multi_insert = True
#         else:
#             multi_insert = False
        
#         try:
#             if hasattr(item, 'handleInsert'):
#                 query = data_to_query(content['table'], getattr(item, 'handleInsert')(content), multi_insert = multi_insert, content['conflict_do_nothing'])
#                 postgreInstance.run_query(query)
#             else:
#                 query = data_to_query(content['table'], content['info'], multi_insert=multi_insert, content['conflict_do_nothing'])
#                 postgreInstance.run_query(query)
#             # logging.info('pipeline : insert : ' + content['data_key'])
#         except:
#             if hasattr(item, 'handleUpdate'):
#                 updateContent = getattr(item, 'handleUpdate')(content)['info']
#                 query = data_to_query(content['table'], updateContent, multi_insert = False, conflict_do_nothing = None)
#                 postgreInstance.run_query(query)
#                 # if "_id" in updateContent['$set']:
#                 #     postgreInstance.updateContentFree({'_id': updateContent['$set']['_id']}, updateContent)
#                 #     logging.info('pipline : update : ' + updateContent['$set']['_id'])
#                 # else:
#                 #     postgreInstance.updateContentFree({'_id': content['_id']}, updateContent)
#                 #     logging.info('pipline : update : ' + content['_id'])



                # self.db.run_query(self.data_to_query("raw_data.worker_failed_info", error_data, multi_insert = False))
#     def close_spider(self, spider):
#         for className in self.postgreDict.keys():
#             self.postgreDict[className].close()

class DefaultValuesPipeline(object):

    def __init__(self):
        self.setting_name_map = {
                                'tokopedia_category': SPIDER_SETTING['tokopedia'],
                                'lazada_category': SPIDER_SETTING['lazada'],
                                'shopee_category': SPIDER_SETTING['shopee']
                                }

    def process_item(self, item, spider):
        content = ItemAdapter(item)
        worker_name = item.__class__.__name__
        try:
            setting = self.setting_name_map.get(worker_name)
        except:
            pass
        if setting:
            worker_type = worker_name.split('_')[-1]
            item.setdefault('db', setting['db'])
            item.setdefault('schema', setting['schema'])
            item.setdefault('created_at', str(datetime.now()))
            item.setdefault('venture', setting['venture'])
            item.setdefault('platform', setting['platform'])

            if content.get('info'): #Products info
                item.setdefault('table', setting[worker_type]['table'])
            elif content.get('failed_url'): #Error info
                item.setdefault('table', setting['error'])

            
            
        return item