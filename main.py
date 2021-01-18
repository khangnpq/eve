#coding:utf8
import os
import sys
import traceback
from scrapy.crawler import CrawlerProcess
# from eve.settings_dev import logger
from eve.spiders.eve import EveSpider
from scrapy.utils.project import get_project_settings
import logging
from datetime import datetime
import requests
import json
import re
from configparser import ConfigParser

cwd = os.getcwd()
log_name = '.'.join([datetime.now().strftime('%Y-%m-%d'), 'log'])
log_path = '/'.join([cwd[:cwd.find('eve')+3], 'log', log_name])
file_handler = logging.FileHandler(filename=log_path)
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
                    level=logging.WARNING, 
                    format='%(asctime)s {%(filename)s:%(lineno)d} %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=handlers
                    )
# logger = logging.getLogger('__name__')

def get_request_list(url):

    request_dict = {}
    status_resp = requests.get(url + '/status')
    project_dict = json.loads(status_resp.text)
    num_project = len(project_dict.values())
    total_project = len(list(filter(lambda x: (x > 0), project_dict.values())))
    total_request = sum(project_dict.values())
    if total_request > num_project * 2: 
        max_process = num_project//total_project
    else:
        max_process  = num_project
    for project, request_num in project_dict.items():
        if request_num > 0:
            current_process = 0
            request_dict[project] = {}
            while current_process < max_process:
                request_resp = requests.get(url + '/getdata?project={}&num=2'.format(project))
                request_list = json.loads(request_resp.text)
                if not request_list['urls']:
                    break
                else:
                    for request_meta in request_list['urls']:
                        allowed_domain = re.findall('\w*(?:\.\w*)+', request_meta['url'])[0]
                        if allowed_domain not in request_dict[project]:
                            request_dict[project][allowed_domain] = [request_meta] 
                        else:
                            request_dict[project][allowed_domain].append(request_meta)
                    current_process += 1
    return request_dict

if __name__ == '__main__':
    # if os.path.exists(str(os.getcwd()) + "/log/running.txt"):
    #     logging.error("Current process is not finished yet.")
    # else: 
    #     with open(str(os.getcwd()) + "/log/running.txt", "w+") as file:
    #         pass
    #     request_dict = get_request_list(url='http://13.212.181.246:5000')

    #     process = CrawlerProcess(get_project_settings())
    #     # for _, val in request_dict.items():
    #     #     for allowed_domain, request_list in val.items():
    #     #         process.crawl(EveSpider,
    #     #                       allowed_domains=allowed_domain,
    #     #                       request_list=request_list)
    #     process.crawl(EveSpider)
        
    #     try:
    #         process.start() 
    #     except Exception as e:
    #         logging.error(traceback.format_exc())
    #     os.remove(str(os.getcwd()) + "/log/running.txt")