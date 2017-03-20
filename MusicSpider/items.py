# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class typeItem(scrapy.Item):
    _id = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()

class playListItem(scrapy.Item):
    _id = scrapy.Field()
    list_id = scrapy.Field()
    list_name = scrapy.Field()
    list_play = scrapy.Field()
    # list_comment = scrapy.Field()
    list_collection = scrapy.Field()
    list_creator = scrapy.Field()
    list_creator_id = scrapy.Field()
    list_tag = scrapy.Field()
    type = scrapy.Field()

class detailItem(scrapy.Item):
    _id = scrapy.Field()
    music_id = scrapy.Field()
    music_name = scrapy.Field()
    music_album = scrapy.Field()
    music_artist = scrapy.Field()
    music_comment_num = scrapy.Field()
    music_comment = scrapy.Field()

class personItem(scrapy.Item):
    _id = scrapy.Field()
    person_id = scrapy.Field()
    person_name = scrapy.Field()
    person_fan = scrapy.Field()
    person_follow = scrapy.Field()
    person_music_play = scrapy.Field()
    person_age = scrapy.Field()
    person_address = scrapy.Field()
    person_event = scrapy.Field()

