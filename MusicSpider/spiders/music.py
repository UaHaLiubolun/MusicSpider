#coding=utf-8
import scrapy
import demjson
from ..items import playListItem, detailItem
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisSpider
from ..validate import validate

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

    def test_parse(self, response):
        print response.body

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
            list_id = selector.xpath("//li[" + str(i)
                                             + "]//a[@class='icon-play f-fr']/@data-res-id").extract_first()
            i = i + 1
            yield scrapy.Request(url=start_url+"/playlist?id="+list_id, method="GET", callback=self.play_list_parse,
                                 meta={"cat": response.meta['cat'], "id": list_id})

    def play_list_parse(self, response):
        start_url = "http://music.163.com"
        item = playListItem()
        selector = Selector(text=response.body)
        item['list_play'] = int(selector.xpath("//strong[@id='play-count']/text()").extract_first())
        item['list_collection'] = int(selector.xpath("//a[@class='u-btni u-btni-fav ']/@data-count").extract_first())
        item['list_comment'] = int(selector.xpath("//span[@id='cnt_comment_count']/text()").extract_first())
        item['list_name'] = selector.xpath("//h2[@class='f-ff2 f-brk']/text()").extract_first()
        item['list_id'] = response.meta['id']
        item['list_tag'] = selector.xpath("//a[@class='u-tag']/i/text()").extract()
        item['list_creator'] = selector.xpath("//span[@class='name']/a/text()").extract_first()
        item['list_creator_id'] = selector.xpath("//span[@class='name']/a/@href").extract_first()
        item['type'] = response.meta['cat']
        # urls = selector.xpath("//ul[@class='f-hide']/li/a/@href").extract()
        # for url in urls:
        #     yield scrapy.Request(url=start_url + url, method="GET", callback=self.detail_parse)
        yield item

    def detail_parse(self, response):
        selector = Selector(text=response.body)
        id = selector.xpath("//div[@id='content-operation']/@data-rid").extract_first()
        detail = validate.Validate(str(id))
        info = demjson.decode(detail.get_music_json())
        if info['total'] > 10000:
            item = detailItem()
            item['music_id'] = id
            item['music_name'] = selector.xpath("//em[@class='f-ff2']/text()").extract_first()
            item['music_album'] = selector.xpath("//p[@class='des s-fc4']/a/text()").extract_first()
            item['music_artist'] = selector.xpath("//p[@class='des s-fc4']/span/@title").extract_first()
            item['music_comment_num'] = int(info['total'])
            item['music_comment'] = info['hotComments']
            yield item














