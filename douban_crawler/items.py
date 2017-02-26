# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#from scrapy.contrib.loader import ItemLoader
#from scrapy.contrib.loader.processor import TakeFirst, Join, MapCompose
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, MapCompose


class DoubanCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    director = scrapy.Field()
    script_writer = scrapy.Field()
    actor = scrapy.Field()
    film_type = scrapy.Field()
    #produced_zone = scrapy.Field()
    #language = scrapy.Field()
    show_date = scrapy.Field()
    show_time = scrapy.Field()
    score = scrapy.Field()
    other_name = scrapy.Field()
    #comment = scrapy.Field()
    comment_people_cnt = scrapy.Field()
    tags = scrapy.Field()
    also_likes = scrapy.Field()
    seen_cnt = scrapy.Field()
    wish_cnt = scrapy.Field()
    comment_cnt = scrapy.Field()
#pass

class DoubanItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    review_in = MapCompose(lambda x: x.replace("\n", " "))
    review_out = Join()

