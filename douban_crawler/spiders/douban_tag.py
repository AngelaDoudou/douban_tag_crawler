# -*- coding: utf-8 -*-
import scrapy
import time
from douban_crawler.items import DoubanCrawlerItem
from douban_crawler.items import DoubanItemLoader

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class DoubanTagSpider(scrapy.Spider):
    name = 'douban-tag'
    allowed_domain=['douban.com']
    #减慢爬取速度 为5s
    download_delay = 5
    start_urls=[
            'https://movie.douban.com/tag/2016',
            ]
    def parse(self, response):
        for item in response.xpath('//*[@class="article"]/div[2]/table'):
            url = item.xpath('tr/td[@valign="top"]/div/a/@href').extract_first()
            other_name = item.xpath('tr/td[@valign="top"]/div/a/span/text()').extract_first()
            if url is not None:
                yield scrapy.Request(url, callback=self.parse_json_item, meta={'other':other_name})
        next_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        time.sleep(self.download_delay)
        if next_url is not None:
            print 'next:' + next_url
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            print 'cant find next page:' + response.url

    def parse_json_item(self, response):
        print response.status
        delim = '/'
        tmp = '#'
        item = DoubanCrawlerItem()
        item['name']=response.xpath('//*[@id="content"]/h1/span[@property="v:itemreviewed"]/text()').extract_first()
        item['director']=delim.join(response.xpath('//*[@id="info"]/span[1]/span[@class="attrs"]/a/text()').extract())
        item['script_writer']=delim.join(response.xpath('//*[@id="info"]/span[2]/span[@class="attrs"]/a/text()').extract())
        item['actor']=delim.join(response.xpath('//*[@class="actor"]/span[@class="attrs"]/a/text()').extract())
        item['film_type']=delim.join(response.xpath('//*[@id="info"]/span[@property="v:genre"]/text()').extract_first())
        #item['produced_zone']=
        #item['language']=response.xpath()
        item['show_date']=delim.join(response.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()').extract())
        item['show_time']=response.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()').extract_first()
        item['other_name']=response.meta['other']
        item['score']=response.xpath('//*[@class="rating_self clearfix"]/strong/text()').extract_first()
        '''
        item['comment']=tmp.join(response.xpath('//*[@id="info"]/text()').extract())
        print len(response.xpath('//*[@id="info"]/text()').extract())
        for it in response.xpath('//*[@id="info"]/text()'):
            print len(it.extract_first())
        '''
        item['comment_people_cnt']=response.xpath('//*[@class="rating_people"]/span/text()').extract_first()
        item['tags']=delim.join(response.xpath('//*[@class="tags-body"]/a/text()').extract())
        item['also_likes']=delim.join(response.xpath('//*[@id="recommendations"]/div/dl/dd/a/text()').extract())
        item['seen_cnt']=response.xpath('//*[@id="subject-others-interests"]/div/a[1]/text()').extract_first()
        item['wish_cnt']=response.xpath('//*[@id="subject-others-interests"]/div/a[2]/text()').extract_first()
        item['comment_cnt']=response.xpath('//*[@id="comments-section"]/div[@class="mod-hd"]/h2/span/a/text()').extract_first()
        #print item
        yield item

