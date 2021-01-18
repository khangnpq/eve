# coding:utf8
import re
import copy
import random
from configparser import ConfigParser
from eve.items.items import Products, ErrorInfo
import scrapy
import json

def proxy_generator(): 
    # read config file
    parser = ConfigParser()
    parser.read('eve/resources/credentials.ini')
    if parser.has_section('proxy'):
        credentials = dict(parser.items('proxy'))
    session_id = random.random()
    proxy = 'http://{}-session-{}:{}@zproxy.lum-superproxy.io:{}'.format(
                                                                         credentials['username'], 
                                                                         session_id, 
                                                                         credentials['password'], 
                                                                         credentials['port']
                                                                        ) 
    
    return proxy
    
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

def generate_request_arguments(request_meta, SETTING, parse_page, err_parse):

    meta = {}
    for key, val in request_meta.items():
        if key not in ['url', 'request_type', 'use_proxy']:
            meta[key] = val
        elif key == 'url':
            request_url = val
            request_site = re.findall('\w*(?:\.\w*)+', request_url)[0]
        elif key == 'use_proxy':
            if val:
                meta['proxy'] = proxy_generator()
        else:
            request_type = val
            worker_type = request_type[request_type.find('_') + 1:]
        
    request_setting = SETTING[meta['platform']]
    setting = generate_spider_setting(request_setting, request_site, request_url, meta['venture'])
    worker_setting = request_setting[worker_type]
    meta['table'] = worker_setting['table']
    payload = worker_setting.get('payload', '') # Query-based payload

    request = {
               'url': request_url,               
               'callback': parse_page,                 
               'method': worker_setting.get('method', 'GET'),  
               'headers': setting['headers'], 
               'body': json.dumps(payload),          
               'meta': meta,                                                
               'dont_filter': True,                      
               'errback': err_parse
              }                  
    return request

def generate_spider_setting(SETTING, site, url, venture):
    setting = copy.deepcopy(SETTING)
    setting['headers']['referer'] = setting['headers']['referer'].format(site)
    setting['venture'] = venture
    return setting

def generate_item_class(name, field_list, template=Products):
    if isinstance(template, str):
        if template == 'product':
            template = Products
        elif template == 'error':
            template = ErrorInfo
    field_dict = {}
    for field_name in field_list:
        field_dict[field_name] = scrapy.Field()
    return type(name,(template,), field_dict)()


#### LEGACY ####
## TOKOPEDIA

# payload = copy.deepcopy(request_setting.get('payload', ''))
# if url_type == 'tokopedia_category':     
#     cat_id = request_meta.get('sc')
#     row = request_meta.get('row')
#     payload['variables'] = {'params': payload['variables']['params'].format(str(cat_id), 
#                                                                             str(row), 
#                                                                             str((current_page-1)*row+1), 
#                                                                             str(current_page))
#                             }
# elif url_type == 'tokopedia_search':      
#     row = request_meta.get('row')
#     payload['variables'] = {'params': payload['variables']['params'].format(str(current_page), 
#                                                                             str(request_meta.get('keyword')), 
#                                                                             str(row),
#                                                                             str((current_page-1)*row)), 

# def data_to_query(table, data, multi_insert = False, conflict_do_nothing = None): 
        
#     if multi_insert == False: 
#         columns = ""
#         values = ""
#         for key, value in list(data.items()):
#             columns = columns + str(key) + ", "
#             values = values + "'" + str(value).replace("'", '"') + "'" + ", "

#         columns = columns[:-2]
#         values = "(" + values[:-2] + ")"

#         query = "INSERT INTO {} ({}) VALUES {}".format(table, columns, values)

#         if conflict_do_nothing != None: 
#             query = query + ' ON CONFLICT ({}) DO NOTHING'.format(",".join(conflict_do_nothing)) 


#     elif len(data) > 0: 
#         values = ""
#         columns = ", ".join(list(data[0].keys()))
#         multi_values = "" 

#         for diction in data: 
#             for key, value in list(diction.items()):
#                 values = values + "'" + str(value).replace("'", '"') + "'" + ", "

#             multi_values = multi_values + "(" + values[:-2] + "), " 
#             values = ""

#         query = "INSERT INTO {} ({}) VALUES {}".format(table, columns, multi_values[:-2])

#         if conflict_do_nothing != None: 
#             query = query + ' ON CONFLICT ({}) DO NOTHING'.format(",".join(conflict_do_nothing)) 
        
#     return query 
