# -*- coding: utf-8 -*-
import scrapy
from lxml import etree  # 修正字符串
from lxml.html import fromstring  # response对象与lxml 结合在一起使用
from queue import Queue  # 队列管道
from pyquery import PyQuery
import threading  # 多线程
import re


class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://chengdu.anjuke.com/']

    def parse(self, response):

        # selector = etree.HTML(response)
        # print(etree.tostring(a))

        # selector = response.xpath('//div[@id="city-panel"]/dl/dd/a/@href')
        selector = fromstring(response.body.decode())
        region_url_list = selector.xpath('//div[@id="city-panel"]/dl/dd/a/@href')

        for url in region_url_list:

            yield scrapy.Request(
                url,
                callback=self.city_dispose
            )
        print('抓取ok')

    def city_dispose(self, response):
        retes_url = response.xpath('//a[text()="房 价"]/@href').extract_first()
        # print(retes_url)

        if retes_url:
            yield scrapy.Request(
                retes_url,
                callback=self.rates_trend
            )

    def rates_trend(self, response):
        item = dict()

        # print('查看详情请求完整的url路径: ', response.request.url)
        # print('查看详情响应完整的url路径: ', response.url)

        #  解码unicode明文
        # .encode("utf-8").decode('unicode_escape')
        # rates_trend = re.findall(r"drawChart\(\{\s+id:'regionChart',\s+.*\s+.*\s+(.*)\s+(.*)", response.body.decode())

        rates_trend = re.compile(r"drawChart\(\{\s+id:'regionChart',\s+.*\s+.*\s+(.*)\s+(.*)")
        rates_trend = rates_trend.findall(response.body.decode())

        if len(rates_trend) == 1:
            month = re.findall(r'[0-9]+月', rates_trend[0][0].encode("utf-8").decode('unicode_escape'))
            year = re.findall(r'\d+年', rates_trend[0][0].encode("utf-8").decode('unicode_escape'))
            money = re.findall(r'\d+', rates_trend[0][1].encode("utf-8").decode('unicode_escape'))

            rates_trend_money = [year[x] + month[x] + ':' + money[x] for x in range(len(month))]
            city_rates_trend = response.xpath('//div[@class="priceTrend"]/h1/text()').extract_first()

            if city_rates_trend:
                item[city_rates_trend] = rates_trend_money

                yield item