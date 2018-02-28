#!/usr/bin/python
#coding:utf-8

from scrapy import Request
from scrapy.spiders import Spider
from bosszhipin.items import CityInfoItem
import re

#爬取城市名
class CitySpider(Spider):
    name = 'city'
    #通过这个默认设置，可以不用在setting文件中设置ITEM_PIPELINES
    custom_settings = {
        'ITEM_PIPELINES': {'bosszhipin.pipelines.CityInfoPipeline': 300}
    }

    def start_requests(self):
        url = 'https://www.zhipin.com/c101010100-p100104/?page=1'
        yield Request(url)

    def parse(self, response):
        item = CityInfoItem()
        cases = response.xpath('.//*[@id="filter-box"]/div/div[2]/dl[1]/dd/a')
        for case in cases:
            #获取城市名
            item['city_name'] = case.xpath('.//text()').extract()[0]
            if (item['city_name'] == '不限'):
                continue
            #获取城市url
            city_url_str = case.xpath('.//@href').extract()[0]
            match = re.match(r'^/(.*)-', city_url_str)
            if (match == None):
                pass
            else:
                item['city_url'] = match.group(1)
            item['city_type'] = 1  #1代表城市
            yield item



