# coding:utf8
from bitk import PostgreSQLConnector
from datetime import datetime
import json
import re
import sys
import pathlib
path = '/'.join(str(pathlib.Path(__file__).parent.absolute()).split('/')[:-1])
sys.path.insert(1, path)
from dbs.postgre import PostgreSQLClient
from scripts.scripts import data_to_query, escape

def generate_result(rows):
    data = []
    for index, row in rows.iterrows():
        try:
            product_list = json.loads(row['data']).get('items') #json.loads(row['data']).get('items')
        except:
            text = str(row['data'])
            text = re.sub(r'("name":")([\s\S]*?)(",")', lambda x: x.group(1) + escape(x.group(2)) + x.group(3), text)
            text = re.sub(r'("brand":")(.*?)(","?)', lambda x: x.group(1) + escape(x.group(2)) + x.group(3), text)
            text = re.sub(r'("tier_variations":\[{)(.*?)(}\])', lambda x: x.group(1) + x.group(3), text)
            text = re.sub(r'("exclusive_price_info":)(.*?)(,"name"?)', lambda x: x.group(1) + 'null' + x.group(3), text)
            text = text.replace(':00,', ':0,')
            try:
                product_list = json.loads(text).get('items')
            except:
            #     # pass
                print(text)
        position = 1
        for product in product_list:
            info = {
                    'id': row.get('id'),
                    'venture': row.get('venture'),
                    'platform': row.get('platform'), 
                    'created_at': row.get('created_at'), 
                    'cat_1': row.get('cat_1'),
                    'ncat_1': row.get('ncat_1'),
                    'cat_2': row.get('cat_2'),
                    'ncat_2': row.get('ncat_2'),
                    'ncat_3': row.get('ncat_3'),
                    'shop_id': product.get('shopid', 'N/A'),
                    'product_id': product.get('itemid', 'N/A'),
                    'product_name': product.get('name', 'N/A'),
                    'product_url': 'https://shopee.vn/i-i.{}.{}'.format(product.get('shopid', 'N/A'), 
                                                                        product.get('itemid', 'N/A')),
                    'original_price': product.get('price_before_discount', 'N/A') // 10**5,
                    'sale_price': product.get('price', 'N/A') // 10**5,
                    'discount': product.get('discount', 'N/A') if product.get('discount', 'N/A') != None else "0%",
                    'historical_sold': product.get('historical_sold', 'N/A') if \
                                       product.get('historical_sold', 'N/A') != None else 0,
                    'view_count': product.get('view_count', 'N/A'),
                    'cmt_count': product.get('cmt_count', 'N/A'),
                    'liked_count': product.get('liked_count', 'N/A'),
                    'ctime': product.get('ctime', 'N/A'),
                    'page': row.get('page'),
                    'position': position
                    }
            position += 1
            data.append(info)
    return data

if __name__ == '__main__':
    db = PostgreSQLClient('eve')
    for start in range(4135, 8400, 100):
        rows = db.run_query(''' WITH step_1 AS(
                                SELECT
                                        sc."id",
                                        sc."venture",
                                        sc."platform",
                                        sc."created_at",
                                        sc."data",
                                        sc."page",
                                        cat."cat_1",
                                        sc."cat_id" AS "cat_2",
                                        sc."keyword" AS "ncat_3"
                                FROM 
                                    "DS-3_raw_data"."shopee_category" sc,
                                        "task_manager"."category" cat
                                WHERE
                                        sc.cat_id::BIGINT = cat.cat_2::BIGINT
                                )
                                SELECT
                                        s1.*,
                                        cm1.cat_name AS "ncat_1",
                                        cm2.cat_name AS "ncat_2"
                                FROM
                                        step_1 s1
                                LEFT JOIN
                                        "task_manager"."cat_mapping" cm1
                                    ON
                                        cm1.cat_id::BIGINT = s1.cat_1::BIGINT
                                LEFT JOIN
                                        "task_manager"."cat_mapping" cm2
                                    ON
                                        cm2.cat_id::BIGINT = s1.cat_2::BIGINT	
                                WHERE
                                    s1."id" BETWEEN {} AND {}
                            '''.format(start, start + 99), 
                            return_data=True)
        data = generate_result(rows)
        # print(data)
        db.run_query(data_to_query('"DS-3_cleaned_data"."shopee_category"', data, multi_insert = True))
    db.disconnect()