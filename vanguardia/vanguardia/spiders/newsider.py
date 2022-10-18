from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

SAVE_PATH = r'C:\DISCO L\Laury\Escuela\Universidad\Quinto año\TESIS\Code\Metaphor-Detection\vanguardia\vanguardia\news\\'

class NewSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['www.vanguardia.cu']
    start_urls = ['http://www.vanguardia.cu']
    rules = [Rule(LinkExtractor(),callback='parse', follow=True)]



    def parse(self, response):
        tile_area = response.css('body > div > div > main > div > div.panel.panel-default.intro-content > div > div.item-title > h1').get()
        date_area = response.css('body > div > div > main > div > div.panel.panel-default.intro-content > div > div.item-info > div.createdate > time').get()
        text_area = response.css('body > div > div > main > div > div.panel.panel-default.full-content > div.col-xs-12.col-sm-12.col-md-11.content > div').get()
        if tile_area is not None and date_area is not None and text_area is not None:
            title = tile_area.split('\t')[3]
            date = date_area.split('\t')[4].split('</i>')[-1]
            text = ' '.join(text_area.split('<p>')[1:])
            path = SAVE_PATH + date + '-' + title + '.txt'
            with open(path, 'w', encoding='utf-8') as file:
                file.write(text)


