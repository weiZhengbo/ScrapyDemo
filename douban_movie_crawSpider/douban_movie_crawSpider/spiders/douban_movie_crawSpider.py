# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from douban_movie_crawSpider.items import DoubanMovieCrawspiderItem
from scrapy.http import Request


class MoiveSpider(CrawlSpider):
    name = "douban_movie_crawSpider"
    allowed_domains = []
    start_urls = ["https://movie.douban.com/top250"]

    rules = [
        #Rule(LinkExtractor(allow=r'.*/subject/.*'), callback='parse_item')
        #Rule(LinkExtractor(allow=('subject/\d+/$',)), callback='parse_item')
        Rule(LinkExtractor(allow=('https://movie.douban.com/hahaha/\d+')), callback='parse_item')
       # Rule(LinkExtractor(allow=(r' ^ https: // book.douban.com / subject /[0-9] * / '),), callback ='parse_item', follow = False)
        #Rule(LinkExtractor(restrict_xpaths='//div[@class="hd"]/a/@href'), callback='parse_item', follow=True)
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Host': 'movie.douban.com'
    }

    def start_requests(self):
        # return [Request(url=self.start_urls[0], callback=self.parse_item, headers=self.headers)]
        return [scrapy.Request(url=self.start_urls[0],
                               headers=self.headers,
                               callback=self.parse_item,
                               dont_filter=True)]

    def parse_item(self, response):
        pre = 'https://movie.douban.com/top250'
        sel = Selector(response)
        # item = DoubanMovieCrawspiderItem()
        # print(sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract())
        # item['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        # item['year'] = sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        # item['score'] = sel.xpath('//*[@id="interest_sectl"]/div/p[1]/strong/text()').extract()
        # item['director'] = sel.xpath('//*[@id="info"]/span[1]/a/text()').extract()
        # item['classification'] = sel.xpath('//span[@property="v:genre"]/text()').extract()
        # item['actor'] = sel.xpath('//*[@id="info"]/span[3]/a[1]/text()').extract()
        urls1 = sel.xpath('//div[@class="hd"]/a/@href').extract()
        urls2 = sel.xpath('//span[@class="next"]/a/@href').extract()
        for i in range(len(urls1)):
            print(urls1[i])
            yield Request(urls1[i], headers=self.headers, callback=self.parse_item2)
        print("页面结束")
        for i in range(len(urls2)):
            print(pre + urls2[i])
            yield Request(pre + urls2[i], headers=self.headers, callback=self.parse_item)
        #yield item

    def parse_item2(self, response):
        sel = Selector(response)
        item = DoubanMovieCrawspiderItem()
        item['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year'] = sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score'] = sel.xpath('//*[@class="ll rating_num"]/text()').extract()
        item['director'] = sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['classification'] = sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor'] = sel.xpath('//*[@id="info"]/span[3]/span[2]/span/a/text()').extract()
        # print(url)
        yield item

    def parse_start_url(response):
        print("进入")
        pre = 'https://movie.douban.com/top250'
        urls = response.xpath('//span[@class="next"]/a/@href').extract()
        for url in urls:
            if 'https' not in url:  # 去除多余的链接
                url = pre + url  # 补全
                print(url)
                print('*' * 30)
                yield scrapy.Request(url)
