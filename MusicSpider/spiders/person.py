#coding=utf-8
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import re
import time
from ..items import personItem
from scrapy_redis.spiders import RedisSpider
from scrapy import Request
from scrapy.selector import Selector

class PersonSpider(RedisSpider):
    name = "person"
    redis_key = 'person:urls'

    def start_requests(self):
        for i in range(20):
            if i != 0:
                num = i * 50000000
                yield Request(url="http://music.163.com/user/home?id=" + str(num), callback=self.parse, meta={"id": num})
        # yield Request(url="http://music.163.com/user/home?id=1", callback=self.parse, meta={"id": 1})
        # yield Request(url="http://music.163.com/user/home?id=1000000", callback=self.parse, meta={"id": 1000000})
        # yield Request(url="http://music.163.com/user/home?id=5000000", callback=self.parse, meta={"id": 5000000})
        # yield Request(url="http://music.163.com/user/home?id=10000000", callback=self.parse, meta={"id": 10000000})
        # yield Request(url="http://music.163.com/user/home?id=15000000", callback=self.parse, meta={"id": 1500000})
        # yield Request(url="http://music.163.com/user/home?id=20000000", callback=self.parse, meta={"id": 20000000})
        # yield Request(url="http://music.163.com/user/home?id=25000000", callback=self.parse, meta={"id": 25000000})
        # yield Request(url="http://music.163.com/user/home?id=30000000", callback=self.parse, meta={"id": 30000000})
        # yield Request(url="http://music.163.com/user/home?id=40000000", callback=self.parse, meta={"id": 40000000})
        # yield Request(url="http://music.163.com/user/home?id=50000000", callback=self.parse, meta={"id": 50000000})
        # yield Request(url="http://music.163.com/user/home?id=60000000", callback=self.parse, meta={"id": 60000000})
        # yield Request(url="http://music.163.com/user/home?id=70000000", callback=self.parse, meta={"id": 70000000})
        # yield Request(url="http://music.163.com/user/home?id=80000000", callback=self.parse, meta={"id": 80000000})
        # yield Request(url="http://music.163.com/user/home?id=90000000", callback=self.parse, meta={"id": 90000000})
        # yield Request(url="http://music.163.com/user/home?id=100000000", callback=self.parse, meta={"id": 100000000})
        # yield Request(url="http://music.163.com/user/home?id=150000000", callback=self.parse, meta={"id": 150000000})
        # yield Request(url="http://music.163.com/user/home?id=200000000", callback=self.parse, meta={"id": 200000000})
        # yield Request(url="http://music.163.com/user/home?id=300000000", callback=self.parse, meta={"id": 300000000})
        # yield Request(url="http://music.163.com/user/home?id=400000000", callback=self.parse, meta={"id": 400000000})
        # yield Request(url="http://music.163.com/user/home?id=500000000", callback=self.parse, meta={"id": 500000000})
        # yield Request(url="http://music.163.com/user/home?id=600000000", callback=self.parse, meta={"id": 600000000})
        # yield Request(url="http://music.163.com/user/home?id=700000000", callback=self.parse, meta={"id": 700000000})
        # yield Request(url="http://music.163.com/user/home?id=800000000", callback=self.parse, meta={"id": 800000000})
        # yield Request(url="http://music.163.com/user/home?id=900000000", callback=self.parse, meta={"id": 900000000})
        # yield Request(url="http://music.163.com/user/home?id=1000000000", callback=self.parse, meta={"id": 1000000000})



    def parse(self, response):
        selector = Selector(text=response.body)
        address = selector.xpath("//div[@class='inf s-fc3']/span[1]/text()").extract_first()
        age = selector.xpath("//span[@id='age']/@data-age").extract_first()
        fans = selector.xpath("//strong[@id='fan_count']/text()").extract_first()
        follow = selector.xpath("//strong[@id='follow_count']/text()").extract_first()
        event = selector.xpath("//strong[@id='event_count']/text()").extract_first()
        count = selector.xpath("//h4/text()").extract_first()
        name = selector.xpath("//span[@class='tit f-ff2 s-fc0 f-thide']/text()").extract_first()

        id = response.meta["id"] - 1
        yield Request(url="http://music.163.com/user/home?id=" + str(id), callback=self.parse, meta={"id": id})
        if name != None:
            id = response.meta["id"]
            item = personItem()
            item['person_name'] = name
            if age != None:
                age = int(age) / 1000
                age = time.gmtime(int(age))
                age = time.strftime("%Y-%m-%d %H:%M:%S", age)
                item['person_age'] = age
            if address != None:
                address = address.replace(" ", "")
                item['person_address'] = address.split("：")[1].split("-")
            if count != None:
                music_count = re.sub('\D', '', count)
                item['person_music_play'] = int(music_count)
            item['person_follow'] = int(follow)
            item['person_fan'] = int(fans)
            item['person_event'] = int(event)
            item['person_id'] = id
            yield item


