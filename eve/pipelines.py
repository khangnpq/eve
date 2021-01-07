# -*- coding: utf-8 -*-
import sys
import platform
import logging
import copy
from itemadapter import ItemAdapter
from datetime import datetime
from eve.dbs.postgre import PostgreSQLClient
from eve.scripts.scripts import *
from eve.resources.definitions import * 

class EvePipeline(object):
    def __init__(self):
        self.postgreDict = {}
        self.data = {}

    def _getPostgreInstance(self, item):
        dbname_platform_wtype = item.__class__.__name__
        database_name = 'eve'
        if database_name not in self.postgreDict:
            self.postgreDict[database_name] = PostgreSQLClient(database_name)
        return self.postgreDict[database_name]

    def process_item(self, item, spider):
        postgreInstance = self._getPostgreInstance(item)
        content = ItemAdapter(item)
        db_name = 'eve'
        # try:
        if hasattr(item, 'handleInsert'):
            info = getattr(item, 'handleInsert')(content)
            table_name = '"{}"'.format(content['schema']) + '.' + '"{}"'.format(content['table'])
            if db_name not in self.data:
                self.data[db_name] = {}
            if table_name not in self.data[db_name]:
                self.data[db_name][table_name] = []
            if info['data'] not in self.data[db_name][table_name]:
                self.data[db_name][table_name].append(info)
            new_data = copy.deepcopy(self.data)
            for db in new_data.keys():
                for table in new_data[db].keys():    
                    if len(self.data[db][table]) == 50:
                        query = data_to_query(table, self.data[db][table], multi_insert = True)
                        postgreInstance.run_query(query)
                        logging.info('pipeline : insert into ' + content['schema'] + '.' + content['table'] + ' success!')
                        self.data[db][table].clear()
                        self.data[db].pop(table, None)
                if len(self.data[db].keys()) == 0:
                    self.data.pop(db, None)
            del new_data
            # else:
            #     query = data_to_query(content['table'], content['info'], multi_insert=multi_insert, content['conflict_do_nothing'])
            #     postgreInstance.run_query(query)
            
        # except:
        #     pass
            # if hasattr(item, 'handleUpdate'):
            #     updateContent = getattr(item, 'handleUpdate')(content)['info']
            #     query = data_to_query(content['table'], updateContent, multi_insert = False, conflict_do_nothing = None)
            #     postgreInstance.run_query(query)
                # if "_id" in updateContent['$set']:
                #     postgreInstance.updateContentFree({'_id': updateContent['$set']['_id']}, updateContent)
                #     logging.info('pipline : update : ' + updateContent['$set']['_id'])
                # else:
                #     postgreInstance.updateContentFree({'_id': content['_id']}, updateContent)
                #     logging.info('pipline : update : ' + content['_id'])

        # self.db.run_query(self.data_to_query("raw_data.worker_failed_info", error_data, multi_insert = False))
    def close_spider(self, spider):
        for database_name in self.postgreDict.keys():
            postgreInstance = self.postgreDict[database_name]
            new_data = copy.deepcopy(self.data)
            for db in new_data.keys():
                for table in new_data[db].keys():    
                    if self.data[db][table]:
                        query = data_to_query(table, self.data[db][table], multi_insert = True)
                        postgreInstance.run_query(query)
                        self.data[db][table].clear()
                        self.data[db].pop(table, None)
                if len(self.data[db].keys()) == 0:
                    self.data.pop(db, None)
            del new_data
            self.postgreDict[database_name].disconnect()

class DefaultValuesPipeline(object):

    def process_item(self, item, spider):
        content = ItemAdapter(item)
        item_name = item.__class__.__name__
        project_name = item_name.split('_')[0]
        platform = item_name.split('_')[1]
        try:
            setting = SPIDER_SETTING[project_name][platform]
        except:
            pass
        if setting:
            worker_type = '_'.join(item_name.split('_')[2:])
            item.setdefault('db', setting['db'])
            item.setdefault('schema', setting['schema'])
            item.setdefault('created_at', datetime.now())
            item.setdefault('venture', setting['venture'])
            item.setdefault('platform', platform)

            if content.get('info'): #Products info
                item.setdefault('table', setting[worker_type]['table'])
            elif content.get('failed_url'): #Error info
                item.setdefault('table', setting['error'])
            
        return item