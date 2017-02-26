# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs

from scrapy import signals
#from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exporters import CsvItemExporter

class DoubanCrawlerPipeline(object):
    def __init__(self):
        self.file = codecs.open('douban_crawler.json', mode = 'wb', encoding = 'utf-8')

    def process_item(self,item,spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape"))
        return item

class DoubanCrawlerCsvPipeline(object):
    def __init__(self):
        self.file={}
        
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline
    def spider_opened(self, spider):
        #self.file = codecs.open('output.csv', mode='wb', encoding='utf-8')
        self.file = open('%s_items_2016.csv' % spider.name,'w+b')
        self.exporter = CsvItemExporter(self.file, include_headers_line=True)
        #self.exporter = DoubanCsvItemExporter(self.file, include_headers_line=True)
        self.exporter.fields_to_export =['name','other_name','director','script_writer','actor','film_type','seen_cnt','wish_cnt','show_date','show_time','score','comment_cnt','comment_people_cnt','also_likes','tags']
        self.exporter.start_exporting()
    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

