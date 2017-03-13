# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from items import typeItem
from items import playListItem
from pymongo import MongoClient

class MusicspiderPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DB']
        client = MongoClient(host, port)
        tdb = client[db_name]
        self.post = tdb[db_name]


    def process_item(self, item, spider):
        if isinstance(item, typeItem):
            try:
                type_info = dict(item)
                if self.post.find_one({'type':item['type']}):
                    pass
                else:
                    if self.post.insert(type_info):
                        print 'ssss'
            except Exception:
                print 'failed'
        elif isinstance(item, playListItem):
            try:
                list_info = dict(item)
                list_id = self.post.find_one({'list_id': item['list_id']})
                if list_id:
                    self.post.update({"list_id": list_id}, list_info)
                else:
                    self.post.insert(list_info)
            except Exception:
                pass
        return item
