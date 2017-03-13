#coding=utf-8
import scrapy
import re
from ..items import playListItem
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisSpider

class MusicSpider(RedisSpider):
    name = 'music'
    start_urls = 'http://music.163.com/discover/playlist'
    redis_key = 'music:urls'
    allowed_domains = ["music.163.com"]


    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, method='GET', callback=self.parse)

    def parse(self, response):
        body = response.body
        type_list = Selector(text=body).xpath("//a[@class='s-fc1 ']/text()").extract()
        url = 'http://music.163.com/discover/playlist/?cat='
        for tmp in type_list:
            try:
                true_url = url + tmp
                yield scrapy.Request(url=true_url, method="GET",
                                     callback=self.list_parse, meta={"cat": tmp})
            except Exception:
                pass

    def list_parse(self, response):
        selector = Selector(text=response.body)
        list = selector.xpath("//li//a[@class='msk']/@title")
        urls = selector.xpath("//a[@class='zpgi']/@href").extract()
        start_url = "http://music.163.com"
        for tmp_url in urls:
            yield scrapy.Request(url=start_url + tmp_url, method="GET", callback=self.list_parse,
                                 meta={"cat": response.meta['cat']})
        i = 1
        for tmp in list:
            item = playListItem()
            item['list_name'] = selector.xpath("//li[" + str(i) + "]//a[@class='msk']/@title").extract_first()
            num = selector.xpath("//li[" + str(i) + "]//span[@class='nb']/text()").extract_first()
            if num.isdigit():
                num = int(num)
            else:
                s = re.findall(r'(\w*[0-9]+)\w*', num)
                num = int(s[0]) * 10000

            item['list_num'] = num
            item['list_id'] = selector.xpath("//li[" + str(i)
                                             + "]//a[@class='icon-play f-fr']/@data-res-id").extract_first()
            item['list_creator'] = selector.xpath("//li[" + str(i)
                                                  + "]//a[@class='nm nm-icn f-thide s-fc3']/text()").extract_first()
            item['list_creator_id'] = selector.xpath("//li[" + str(i)
                                                     + "]//a[@class='nm nm-icn f-thide s-fc3']/@href").extract_first()
            item['type'] = response.meta['cat']
            i = i + 1
            yield item




































