# coding:utf8
import json
import re
import copy

def data_to_query(table, data, multi_insert = False, conflict_do_nothing = None): 
        
        if multi_insert == False: 
            columns = ""
            values = ""
            for key, value in list(data.items()):
                columns = columns + str(key) + ", "

                if key == "data":
                    values = values + "'" + str(value).replace("'", '"') + "'" + ", "
                else:
                    values = values + "'" + str(value)+ "'" + ", "

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
                    if key == "data":
                        values = values + "'" + str(value).replace("'", '"') + "'" + ", "
                    else:
                        values = values + "'" + str(value)+ "'" + ", "

                multi_values = multi_values + "(" + values[:-2] + "), " 
                values = ""

            query = "INSERT INTO {} ({}) VALUES {}".format(table, columns, multi_values[:-2])

            if conflict_do_nothing != None: 
                query = query + ' ON CONFLICT ({}) DO NOTHING'.format(",".join(conflict_do_nothing)) 
            
        return query 

def escape(var): 
    string = str(var) 
    string = string.replace('/',  '') 
    string = string.replace('\\',  '') 
    string = string.replace("'", "")
    string = string.replace('"', "") 
    return string 

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
    obj_mirror = obj.copy()
    for path in paths:
        for address in path:
            obj_mirror = obj_mirror[address]
    return obj_mirror

def generate_request_arguments(url, spider_setting, parse_page, err_parse):
    url_type = url.get('url_type')
    platform = url_type.split('_')[0]
    worker_type = '_'.join(url_type.split('_')[1:])
    request_setting = spider_setting[worker_type]
    payload = copy.deepcopy(request_setting.get('payload', ''))
    current_page = url.get('page')
    meta = {'url_type': url_type,
            'project': url.get('project'),
            'worker_type': worker_type,
            'page': current_page} 
    request_url = url.get('url')
    if url_type == 'tokopedia_category':     
        cat_id = url.get('sc')
        row = url.get('row')
        payload['variables'] = {'params': payload['variables']['params'].format(str(cat_id), 
                                                                                str(row), 
                                                                                str((current_page-1)*row+1), 
                                                                                str(current_page))
                                }
    elif url_type == 'lazada_category':
        pass
    elif url_type == 'shopee_category':
        pass
    
    request =  [request_url,                #url
                parse_page,                 #callback
                request_setting['method'],  #method
                spider_setting['headers'],  #headers
                json.dumps(payload),        #body
                None,                       #cookies
                meta,                       #meta
                'utf-8',                    #encoding
                0,                          #priority
                True,                       #dont_filter
                err_parse]                  #errback
    # meta['request'] = request
    # request[6] = meta
    return request

def generate_spider_setting(SETTING, PROJECT, site):
    SETTING['allowed_domains'] = SETTING['allowed_domains'][0].format(PROJECT[site])
    SETTING['start_urls'] = SETTING['start_urls'][0].format(PROJECT[site])
    SETTING['headers']['referer'] = SETTING['headers']['referer'].format(PROJECT[site])
    if site == 'tokopedia':
        venture = 'id'
    else:
        venture = PROJECT[site].split('.')[-1] #lazada.vn -> vn, lazada.co.id -> id
    SETTING['venture'] = venture
    SETTING['db'] = PROJECT['db']
    return SETTING