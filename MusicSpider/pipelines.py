# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from items import typeItem
from items import playListItem, detailItem, personItem
from pymongo import MongoClient

class MusicspiderPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DB']
        client = MongoClient(host, port)
        self.tdb = client["music"]
        # self.post = tdb['demoOne']


    def process_item(self, item, spider):
        if isinstance(item, typeItem):
            try:
                type_info = dict(item)
                post = self.tdb['demo']
                if post.find_one({'type':item['type']}):
                    pass
                else:
                    if post.insert(type_info):
                        print 'ssss'
            except Exception:
                print 'failed'
        elif isinstance(item, playListItem):
            try:
                list_info = dict(item)
                post = self.tdb['play_list']
                list_id = post.find_one({'list_id': item['list_id']})
                if list_id:
                    post.update({"list_id": list_id['list_id']}, list_info)
                else:
                    post.insert(list_info)
            except Exception:
                pass
        elif isinstance(item, detailItem):
            try:
                music_info = dict(item)
                post = self.tdb['music_detail']
                music_id = post.find_one({'music_id': item['music_id']})
                if music_id:
                    post.update({"music_id": music_id['music_id']}, music_info)
                else:
                    post.insert(music_info)
            except Exception:
                    pass
        elif isinstance(item, personItem):
            try:
                person_info = dict(item)
                post = self.tdb['person']
                person_id = post.find_one({'person_id': item['person_id']})
                if person_id:
                    try:
                        post.update({"person_id": person_id['person_id']}, person_info)
                    except Exception:
                        pass
                else:
                    post.insert(person_info)
            except Exception:
                pass
        return item
