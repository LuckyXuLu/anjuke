# -*- coding: utf-8 -*-
import scrapy


class AngukeSpider(scrapy.Spider):
    name = 'anguke'
    allowed_domains = ['anguke.com']
    start_urls = ['http://anguke.com/']

    def parse(self, response):
        pass
