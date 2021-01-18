# coding:utf8
from bitk import PostgreSQLConnector
from datetime import datetime
import json
import re
import sys
import pathlib
from datetime import datetime

path = '/'.join(str(pathlib.Path(__file__).parent.absolute()).split('/')[:-1])
sys.path.insert(1, path)
from dbs.postgre import PostgreSQLClient
from scripts.scripts import data_to_query, escape

def clean_text(text):
    text = re.sub(r'("description":")([\s\S]*?)(",")', lambda x: x.group(1) + escape(x.group(2)) + x.group(3), text)
    text = re.sub(r'("name":")([\s\S]*?)("}*\]*,")', lambda x: x.group(1) + escape(x.group(2)) + x.group(3), text)
    text = re.sub(r'("place":")([\s\S]*?)("}*\]*,")', lambda x: x.group(1) + escape(x.group(2)) + x.group(3), text)
    text = re.sub(r'("display_name":")([\s\S]*?)(",")', lambda x: x.group(1) + escape(x.group(2)) + x.group(3), text)
    text = re.sub(r'("shop_covers":\[{)(.*?)(}\])', lambda x: x.group(1) + x.group(3), text)
    # text = re.sub(r'("exclusive_price_info":)(.*?)(,"name"?)', lambda x: x.group(1) + 'null' + x.group(3), text)
    # text = text.replace(':00,', ':0,')
    return text

def generate_result(rows):
    data = []
    for index, row in rows.iterrows():
        shop_data = clean_text(str(row['data']))
        shop_lop_data = clean_text(str(row['lop_data']))

        shop_lop_data = json.loads(shop_lop_data)
        try:
            shop_data = json.loads(shop_data).get('data')
        except:
            print(shop_data)
        info = {
                'id': row.get('id'),
                'venture': row.get('venture'),
                'platform': row.get('platform'), 
                'created_at': str(row.get('created_at')), 
                'shop_id': row.get('shop_id', 'N/A'),
                'shop_name': shop_data.get('name', 'N/A'),
                'shop_url': 'https://shopee.vn/shop/{}'.format(row.get('shop_id', 'N/A')),
                'following': shop_data.get('account').get('following_count', 'N/A'),
                'followers': shop_data.get('follower_count', 'N/A'),
                'response_rate': '{}%'.format(shop_data.get('response_rate', 'N/A')),
                'response_time': shop_data.get('response_time', 'N/A') if \
                                 shop_data.get('response_time', 'N/A') != None else 0,
                'rating_good': shop_data.get('rating_good', 'N/A'),
                'rating_normal': shop_data.get('rating_normal', 'N/A'),
                'rating_bad': shop_data.get('rating_bad', 'N/A'),
                'rating_star': shop_data.get('rating_star', 'N/A') if \
                               shop_data.get('rating_star', 'N/A') != None else 0,
                'join_date': datetime.fromtimestamp(int(shop_data.get('ctime'))).strftime('%Y-%m-%d %H:%M:%S'),
                'seller_address': shop_data.get('place', 'N/A'),
                'brands': shop_lop_data.get('brands') if \
                          len(shop_lop_data.get('brands')) > 0 else \
                          [{'brandid':114192,'name':'No Brand'}],
                }

        lop_cat_list = shop_lop_data.get('facets')
        product_cat_info = []
        for lop_cat in lop_cat_list:
            cat_info = lop_cat['category']
            if cat_info['parentids'] != None:
                cat_id = ' > '.join(map(str,cat_info['parentids'])) + ' > ' + str(lop_cat['catid'])
            else:
                cat_id = str(lop_cat['catid'])

            product_cat_info.append({
                                     'category': cat_id,
                                     'cat_name': cat_info['display_name'],
                                     'product_count': lop_cat['count'],
                                    })
        info['product_cat_info'] = product_cat_info
        data.append(info)
    return data

if __name__ == '__main__':
    db = PostgreSQLClient('eve')
    for start in range(1800, 58157, 1000):
        rows = db.run_query(''' SELECT 
                                    ss.*,
                                    ssl.data AS "lop_data"
                                FROM 
                                    "DS-3_raw_data"."shopee_shop" ss,
                                    "DS-3_raw_data"."shopee_shop_lop" ssl
                                WHERE
                                    ss."id" = ssl."id"
                                  AND
                                    ss."id" BETWEEN {} AND {}
                            '''.format(start, start + 999), 
                            return_data=True)
        data = generate_result(rows)
        # print(data)
        db.run_query(data_to_query('"DS-3_cleaned_data"."shopee_shop"', data, multi_insert = True))
    db.disconnect()