# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

num = 0


class CompanyResumeJobPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        client = MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        global num
        job_info = dict(item)
        self.post.insert(job_info)
        num = num + 1
        if num % 10 == 0:
            print("[INFO]已采集{}条数据".format(num))
        return item
