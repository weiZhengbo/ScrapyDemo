from scrapy.spiders import Spider

from scrapy.selector import Selector

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["pyspider.org"]
    start_urls = [
        "http://docs.pyspider.org/en/latest/Deployment/",
        "http://docs.pyspider.org/en/latest/Command-Line/"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul/li')
        for site in sites:
            title = site.xpath('a/text()').extract()
            link = site.xpath('a/@href').extract()
            desc = site.xpath('text()').extract()
            print(title)
            print(link)
            print(desc)
