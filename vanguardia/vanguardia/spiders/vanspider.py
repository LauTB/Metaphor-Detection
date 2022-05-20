import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from vanguardia.items import VanguardiaItem


class VanspiderSpider(CrawlSpider):
    name = 'vanspider'
    allowed_domains = ['www.vanguardia.cu']
    start_urls = ['http://www.vanguardia.cu']
    rules = (
    Rule(LinkExtractor(allow = r'/ediciones-impresas'),
         callback = 'parse_item',
         follow = True),
)

    def parse_item(self, response):
        page_number = 1
        file_local_url = response.css(f'ul.list-group:nth-child(1) > li:nth-child({page_number}) > span:nth-child(1) > a:nth-child(1)::attr(href)').get()
        while file_local_url is not None:
            file_url = response.urljoin(file_local_url)
            item = VanguardiaItem()
            item['file_urls'] = [file_url]
            yield item
            page_number += 1
            file_local_url = response.css(f'ul.list-group:nth-child(1) > li:nth-child({page_number}) > span:nth-child(1) > a:nth-child(1)::attr(href)').get()
