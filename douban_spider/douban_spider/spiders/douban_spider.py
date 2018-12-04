# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from douban_spider.items import DoubanSpiderItem

class DoubanSpider(CrawlSpider):
    name = "douban_spider"

    download_delay = "1"

    allowed_domains = ['https://movie.douban.com/top250']

    start_urls = [
        'https://movie.douban.com/top250?start=0&filter='
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Host': 'movie.douban.com'
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//span[@class="next"]')), callback='parse_item', follow=True)
        #Rule(LinkExtractor(allow=r'.*/subject/.*'),callback='parse_item',follow=True)
        #Rule(LinkExtractor(restrict_xpaths='//span[@class="next"]/a'), callback='parse_item', follow=True),
    )
    def start_requests(self):
        #return [Request(url=self.start_urls[0], callback=self.parse_item, headers=self.headers)]
        return [scrapy.Request(url=self.start_urls[0],
                             headers=self.headers,
                             callback=self.parse_item,
                             dont_filter=True)]

    def parse_item(self, response):
        pre = 'https://movie.douban.com/top250'
        print(response)
        sel = Selector(response)
        item = DoubanSpiderItem()

        movie_name = sel.xpath('//span[@class="title"][1]/text()').extract()
        star = sel.xpath('//div[@class="star"]/span[@class="rating_num"]/text()').extract()
        quote = sel.xpath('//p[@class="quote"]/span[@class="inq"]/text()').extract()

        item['movie_name'] = [n for n in movie_name]
        item['star'] = [n for n in star]
        item['quote'] = [n for n in quote]

        urls = sel.xpath('//span[@class="next"]/a/@href').extract()
        for i in range(len(urls)):
            print(i)
            print(pre+urls[i])
            yield Request(pre+urls[i], headers=self.headers, callback=self.parse_item)
        yield item