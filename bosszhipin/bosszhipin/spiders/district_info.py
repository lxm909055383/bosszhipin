#!/usr/bin/python
#coding:utf-8

from scrapy import Request
from scrapy.spiders import Spider
from bosszhipin.items import CityInfoItem
import re
from bosszhipin.model.mysql_db import *

#爬取区名
class DistrictSpider(Spider):
    name = 'district'
    # 通过这个默认设置，可以不用在setting文件中设置ITEM_PIPELINES
    custom_settings = {
        'ITEM_PIPELINES': {'bosszhipin.pipelines.CityInfoPipeline': 300}
    }

    def start_requests(self):
        #########网址用数据库获取的方式
        url_1 = 'https://www.zhipin.com/'
        url_2 = bosszhipin_city_info.select().where(bosszhipin_city_info.type == 1)
        url_3 = '-p100104'
        for i in url_2:
            url = '%s%s%s' % (url_1, i.url, url_3)
            yield Request(url)

    def parse(self, response):
        item = CityInfoItem()
        cases = response.xpath('.//dl[@class="condition-district show-condition-district"]/dd/a')
        for case in cases:
            item['city_name'] = case.xpath('.//text()').extract()[0]
            if (item['city_name'] == '不限'):
                continue
            city_url_str = case.xpath('.//@href').extract()[0]
            match = re.match(r'^/(.*)-', city_url_str)
            if (match == None):
                item['city_url'] = '-'
            else:
                item['city_url'] = match.group(1)
            item['city_type'] = 2   #2代表区
            yield item

