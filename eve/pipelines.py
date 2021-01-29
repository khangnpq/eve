# -*- coding: utf-8 -*-
from datetime import datetime
from collections import defaultdict
import sqlalchemy as sa
from configparser import ConfigParser
import requests
import json
import random
class InsertToDBPipeline(object):
    def __init__(self):
        self.DB_instance = defaultdict(dict)
        self.data = defaultdict(lambda: defaultdict(list))

    def __generate_DB_instance(self, database, schema, table):
        if database not in self.DB_instance:
            parser = ConfigParser()
            parser.read('eve/resources/credentials.ini')
            if parser.has_section(database):
                credentials = parser[database]
            self.DB_instance[database]['engine'] = sa.create_engine('{}://{}:{}@{}:{}/{}'.format(*credentials.values()))
        
        if table not in self.DB_instance[database]:
            meta = sa.MetaData(schema=schema)
            self.DB_instance[database][table] = sa.Table(
                                                       table, 
                                                       meta, 
                                                       autoload=True, 
                                                       autoload_with=self.DB_instance[database]['engine']
                                                       )
        return [c.name for c in self.DB_instance[database][table].columns]

    def process_item(self, item, spider):
        database = item['database']
        schema = item.get('schema')
        table = item['table']
        column_list = self.__generate_DB_instance(database, schema, table)
        info = getattr(item, 'handleInsert')(item, column_list)
        # print(info)
        self.data[database][table].append(info)

    def close_spider(self, spider):
        cleaner = []
        for database, engine_table in self.DB_instance.items():
            engine = engine_table['engine']
            for table, info_list in self.data[database].items():
                table_obj = engine_table[table]
                q_time = len(info_list) // 100
                q_copy = q_time
                with engine.connect() as conn:
                    while q_time > 0:
                        conn.execute(
                                     table_obj.insert(),
                                     info_list[(q_copy - q_time) * 100:((q_copy - q_time) + 1) * 100]
                                    )
                        q_time -= 1
                    else:
                        conn.execute(
                                     table_obj.insert(),
                                     info_list
                                    )
                # task manager add clean raw data task
                cleaner.append(
                                {
                                'database': database,
                                'schema': table_obj.schema,
                                'table': table
                                }
                              )
            engine.dispose()
        # send clean task
        json_dict = {"urls": cleaner}
        requests.post("http://13.212.181.246:5000/submitdata?project=eve_q", data = json.dumps(json_dict))

class DefaultValuesPipeline(object):

    def process_item(self, item, spider):
        item.setdefault('created_at', datetime.now())
        if item.get('data'):
            item.setdefault('is_cleaned', 0)
            item.setdefault('data_key', '{}_{}'.format(random.randint(1,1000), datetime.now()))
        return item