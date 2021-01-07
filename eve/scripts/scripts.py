# coding:utf8
import json
import re
import copy
import random
import sys

def proxy_generator(): 

        username = 'lum-customer-jamalex-zone-static-route_err-pass_dyn'
        password = 'la3ih9r28h2n'
        port = 22225
        session_id = random.random()
        proxy = 'http://{}-session-{}:{}@zproxy.lum-superproxy.io:{}'.format(username, session_id, password, port) 
        
        return proxy

def data_to_query(table, data, multi_insert = False, conflict_do_nothing = None): 
        
        if multi_insert == False: 
            columns = ""
            values = ""
            for key, value in list(data.items()):
                columns = columns + str(key) + ", "
                values = values + "'" + str(value).replace("'", '"') + "'" + ", "

            columns = columns[:-2]
            values = "(" + values[:-2] + ")"

            query = "INSERT INTO {} ({}) VALUES {}".format(table, columns, values)

            if conflict_do_nothing != None: 
                query = query + ' ON CONFLICT ({}) DO NOTHING'.format(",".join(conflict_do_nothing)) 


        elif len(data) > 0: 
            values = ""
            columns = ", ".join(list(data[0].keys()))
            multi_values = "" 

            for diction in data: 
                for key, value in list(diction.items()):
                    values = values + "'" + str(value).replace("'", '"') + "'" + ", "

                multi_values = multi_values + "(" + values[:-2] + "), " 
                values = ""

            query = "INSERT INTO {} ({}) VALUES {}".format(table, columns, multi_values[:-2])

            if conflict_do_nothing != None: 
                query = query + ' ON CONFLICT ({}) DO NOTHING'.format(",".join(conflict_do_nothing)) 
            
        return query 
def escape_list (lis):
    value = []
    for val in lis:
        if type(val) == dict:
            val = escape_dict(val)
        elif type(val) == list:
            val = escape_list(val)
        else:
            value.append(val)
    return value
def escape_dict(diction):
    for key, val in diction.items():
        if type(val) == list:
            val = escape_list(val)
        elif type(val) == dict:
            val = escape_dict(val)
        elif type(val) == str:
            diction[key] = str(val).replace("'", "").replace('"', "").replace('\\',  '')
    return diction
def escape(text):
    remove_list = ''':'"./\;'''
    text = text.replace(r'\u', 'YOUR_MAMA')
    result = "".join(text[i] if text[i] not in remove_list else ' ' for i in range(len(text)))
    result = result.replace('YOUR_MAMA', r'\u')
    return result.strip()

def replace_path(obj, rules):
    for key, val in rules.items():
        obj = re.sub('{}=\d*'.format(key), '{}={}'.format(key, str(val)), obj)
    return obj

def find_path(obj, condition, path=None):

    if path is None:
        path = []    

    # In case this is a list
    if isinstance(obj, list):
        for index, value in enumerate(obj):
            new_path = list(path)
            new_path.append(index)
            for result in find_path(value, condition, path=new_path):
                yield result 

    # In case this is a dictionary
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = list(path)
            new_path.append(key)
            for result in find_path(value, condition, path=new_path):
                yield result 

            if condition == key:
                new_path = list(path)
                new_path.append(key)
                yield new_path 

def find_in_obj(obj, condition):
    paths = find_path(obj, condition)
    results = []
    for path in paths:
        obj_mirror = obj.copy()
        for address in path:
            obj_mirror = obj_mirror[address]
        results.append(obj_mirror)
    return results

def generate_request_arguments(url, SPIDER_SETTING, proxy, parse_page, err_parse):

    url_type = url.get('url_type')
    platform = url_type.split('_')[0]
    project = url.get('project')
    worker_type = '_'.join(url_type.split('_')[1:])
    spider_setting = SPIDER_SETTING[project][platform]
    request_setting = spider_setting[worker_type]
    payload = copy.deepcopy(request_setting.get('payload', '')) 
    meta = {'platform': platform,
            'venture': url.get('venture'),
            'project': project,
            'worker_type': worker_type}

    if url_type == 'shopee_category':
        meta['proxy'] = proxy

    if url.get('shop_id'):
        meta['shop_id'] = url.get('shop_id')

    if url.get('cat_id'):
        meta['cat_id'] = url.get('cat_id')

    if url.get('page'):
        current_page = url.get('page')
        meta['page'] = current_page
    
    if url.get('keyword'):
        meta['keyword'] = url.get('keyword')

    request_url = url.get('url')
    if url_type == 'tokopedia_category':     
        cat_id = url.get('sc')
        row = url.get('row')
        payload['variables'] = {'params': payload['variables']['params'].format(str(cat_id), 
                                                                                str(row), 
                                                                                str((current_page-1)*row+1), 
                                                                                str(current_page))
                                }
    elif url_type == 'tokopedia_search':      
        row = url.get('row')
        payload['variables'] = {'params': payload['variables']['params'].format(str(current_page), 
                                                                                str(url.get('keyword')), 
                                                                                str(row),
                                                                                str((current_page-1)*row)), 
                                                                                
                                }
    elif url_type == 'lazada_category':
        pass
    elif url_type == 'shopee_category':
        pass
    
    request =  {'url': request_url,               
                'callback': parse_page,                 
                'method': request_setting['method'],  
                'headers': spider_setting['headers'], 
                'body': json.dumps(payload),        
                'cookies': None,                   
                'meta': meta,                       
                'encoding': 'utf-8',                    
                'priority': 0,                         
                'dont_filter': False,                      
                'errback': err_parse}                  
    meta['request'] = request
    request['meta'] = meta
    return request, spider_setting

def generate_spider_setting(SETTING, PROJECT, site):
    SETTING['allowed_domains'] = SETTING['allowed_domains'][0].format(PROJECT[site])
    SETTING['start_urls'] = SETTING['start_urls'][0].format(PROJECT[site])
    SETTING['headers']['referer'] = SETTING['headers']['referer'].format(PROJECT[site])
    if site == 'tokopedia':
        venture = 'id'
    else:
        venture = PROJECT[site].split('.')[-1] #lazada.vn -> vn, lazada.co.id -> id
    SETTING['venture'] = venture
    # SETTING['db'] = PROJECT['db']
    return SETTING