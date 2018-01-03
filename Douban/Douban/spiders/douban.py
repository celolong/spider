# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Douban.items import DoubanItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250?start=0&filter=']
    rules = (
        Rule(LinkExtractor(allow=r'\?start=\d+&filter='), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        movie_list = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for movie in movie_list:
            item = DoubanItem()
            item['name'] = movie.xpath('./div/div[2]/div[1]/a/span[1]/text()').extract_first()
            item['score'] = movie.xpath('./div/div[2]/div[2]/div/span[2]/text()').extract_first()
            item['info'] = movie.xpath('./div/div[2]/div[2]/p[1]/text()').extract_first().strip()
            item['desc'] = movie.xpath('./div/div[2]/div[2]/p[2]/span/text()').extract_first()
            yield item
