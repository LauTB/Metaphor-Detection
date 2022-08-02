# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from calendar import month
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline

class VanguardiaPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        #http://www.vanguardia.cu/images/edimpresa/vanguardia/2022/07/04/pag1.pdf
        file_url = request.url.split("/")
        page_num: str = file_url[-1]
        week_num: str = file_url[-2]
        month: str = file_url[-3]
        year: str = file_url[-4]
        file_name: str = year + "-" + month + "-" + week_num + "_" + page_num
        return file_name