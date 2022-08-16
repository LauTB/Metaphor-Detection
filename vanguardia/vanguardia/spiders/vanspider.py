import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from vanguardia.items import VanguardiaItem
class VanSpider(scrapy.Spider):
    name = 'vanspider'
    def __init__(self):
        super(VanSpider,self).__init__()
        self.allowed_domains = ['www.vanguardia.cu']
        self.start_urls = ['http://www.vanguardia.cu/ediciones-impresas']
        self.rules = (
        Rule(LinkExtractor(allow = r'/ediciones-impresas'),#
            callback = 'parse',
            follow = True),)

    def _get_option_value(self, selector):
        return selector.split(">")[0].split('value')[1][2:-1]

    def parse(self, response):
        year_index = 1
        year_selector = response.css(f'#jform_editionyear > option:nth-child({year_index})').get()
        while year_selector:
            year_index +=1
            year = self._get_option_value(year_selector)
            month_index = 1
            month_selector = response.css(f'#jform_editionmonth > option:nth-child({month_index})').get()
            while month_selector:
                month_index += 1
                month = self._get_option_value(month_selector)
                month_selector = response.css(f'#jform_editionmonth > option:nth-child({month_index})').get()
                edition_index = 1
                edition_selector = response.css(f'#jform_number > option:nth-child({edition_index})').get()
                while edition_selector:
                    edition_index += 1
                    edition = self._get_option_value(edition_selector)                    
                    data = {'jform[editionyear]':year, 
                            'jform[editionmonth]':month,
                            'jform[number]': edition,
                            'jform[catid]':'123',
                            'edecbec821f00c12637194a218cd5a6d':'1'}
                    yield scrapy.FormRequest.from_response(response, url=f'http://www.vanguardia.cu/ediciones-impresas?task=edition.search',formcss = '#edition-form', formdata= data,callback= self.parse_edition)
                    edition_selector = response.css(f'#jform_number > option:nth-child({edition_index})').get()
            year_selector = response.css(f'#jform_editionyear > option:nth-child({year_index})').get()
    
    def parse_edition(self, response):
        empty = response.css('body > div > div > main > section > div > h1').get()
        not_found = 'no encontrada'
        if empty is not None and not_found in empty:
            pass
        else:
            page_number = 1
            file_local_url = response.css(f'ul.list-group:nth-child(1) > li:nth-child({page_number}) > span:nth-child(1) > a:nth-child(1)::attr(href)').get()
            while file_local_url is not None:
                file_url = response.urljoin(file_local_url)
                item = VanguardiaItem()
                item['file_urls'] = [file_url]
                yield item
                page_number += 1
                file_local_url = response.css(f'ul.list-group:nth-child(1) > li:nth-child({page_number}) > span:nth-child(1) > a:nth-child(1)::attr(href)').get()
