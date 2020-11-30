import scrapy
from scrapy.spiders import CrawlSpider
from .urls_spider import UrlsSpider


class ManagerSpider(CrawlSpider):
    name = "manager"

    def start_requests(self):
        states = ["ND", "SD", "NE", "KS", "OK", "TX", "NM", "CO", "WY", "MT", "AZ", "UT", "ID", "WA", "OR", "NV", "CA"]
        urls = UrlsSpider(states).run()
        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        data = response.css('table[border="0"] td[align="center"] table')[0].css('td[align="CENTER"]')
        item = scrapy.item.Field()
        item['Account Name'] = data[0].css('b::text').get()
        item['Billing Street'] = "" if data[1].css('::text').get() == None else data[1].css('::text').get()
        item['Phone'] = data[3].css('::text').get()
        item['Billing State'] = data[2].css('::text').get().split(",")[1].split(" ")[1]
        item['Billing City'] = data[2].css('::text').get().split(",")[0]
        item['Billing Code'] = data[2].css('::text').get().split(",")[1].split(" ")[3]
        yield item

