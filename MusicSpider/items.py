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
    list_num = scrapy.Field()
    list_creator = scrapy.Field()
    list_creator_id = scrapy.Field()
    type = scrapy.Field()
