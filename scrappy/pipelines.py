# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrappy.dbs.mongo import MongoDBClient
import logging


class ScrappyPipeline(object):
    def __init__(self):
        self.mongoDict = {}
        self.collection_name_map = {'ScrappyItem': "scrappy"}  #model class name to mongoDB collection

    def _getMongoInstance(self, item):
        itemClassName = item.__class__.__name__
        collection_name = ''
        for className in self.collection_name_map.keys():
            if itemClassName == className:
                collection_name = self.collection_name_map[itemClassName]
        if collection_name not in self.mongoDict:
            self.mongoDict[collection_name] = MongoDBClient(collection_name)
        return self.mongoDict[collection_name]

    def process_item(self, item, spider):
        mongoInstance = self._getMongoInstance(item)
        content = dict(item)
        try:
            if hasattr(item, 'handleInsert'):
                mongoInstance.storeContent(getattr(item, 'handleInsert')(content))
            else:
                mongoInstance.storeContent(content)
            logging.info('pipline : insert : ' + content['_id'])
        except:
            if hasattr(item, 'handleUpdate'):
                updateContent = getattr(item, 'handleUpdate')(content)
                if "_id" in updateContent['$set']:
                    mongoInstance.updateContentFree({'_id': updateContent['$set']['_id']}, updateContent)
                    logging.info('pipline : update : ' + updateContent['$set']['_id'])
                else:
                    mongoInstance.updateContentFree({'_id': content['_id']}, updateContent)
                    logging.info('pipline : update : ' + content['_id'])

    def close_spider(self, spider):
        for className in self.mongoDict.keys():
            self.mongoDict[className].close()
