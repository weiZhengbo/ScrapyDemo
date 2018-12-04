from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from douban_movie.items import DoubanMovieItem


class DoubanMovieSpider(Spider):
    name = "douban_movie_spider"

    allowed_domains = ["douban.com"]

    start_urls = [
        'https://movie.douban.com/chart'
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    def start_requests(self):
        return [Request(url=self.start_urls[0], callback=self.parse, headers=self.headers)]

    def parse(self, response):
        sel = Selector(response)

        movie_name = sel.xpath("//div[@class='pl2']/a/text()").extract()
        movie_url = sel.xpath("//div[@class='pl2']/a/@href").extract()
        movie_star = sel.xpath("//div[@class='pl2']/div/span[@class='rating_nums']/text()").extract()

        item = DoubanMovieItem()
        item['movie_name'] = [n for n in movie_name]
        item['movie_url'] = [n for n in movie_url]
        item['movie_star'] = [n for n in movie_star]

        yield item

        #print(movie_name,movie_star,movie_url)
