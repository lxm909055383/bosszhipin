#!/usr/bin/python
#coding:utf-8

from scrapy import Request
from scrapy.spiders import Spider
from bosszhipin.items import IndustryInfoItem
import re

class IndustrySpider(Spider):
    name = 'industry'
    # 通过这个默认设置，可以不用在setting文件中设置ITEM_PIPELINES
    custom_settings = {
        'ITEM_PIPELINES': {'bosszhipin.pipelines.IndustryInfoPipeline': 500}
    }

    def start_requests(self):
        url = 'https://www.zhipin.com'
        yield Request(url)

    def parse(self, response):
        item = IndustryInfoItem()

        #所有行业大栏内容
        cases_list4 = response.xpath('.//*[@id="main"]/div/div[1]/div/dl[1]/div[2]/div[1]/ul/li')   #一级分类列表，13个
        for i in range(len(cases_list4)):
            my_item4 = cases_list4.xpath('../li[%d]/text()' % (i + 1)).extract()[0]  #按顺序提取一级分类
            cases_list5 = response.xpath('.//*[@id="main"]/div/div[1]/div/dl[1]/div[2]/div[2]/ul[%d]/li' % (i + 1))  # 一级分类对应的二级分类列表(使用相对路径有问题)
            lenth = len(cases_list5)

            for j in range(lenth):
                my_item5 = cases_list5.xpath('../li[%d]/h4/text()' % (j + 1)).extract()[0]
                cases_list6 = cases_list5.xpath('../li[%d]/div/a' % (j + 1))   #二级分类对应的职位列表

                for case6 in cases_list6:
                    item['industry_name'] = case6.xpath('.//text()').extract()[0]
                    industry_url_str = case6.xpath('.//@href').extract()[0]
                    match = re.search(r'-(.*)/', industry_url_str)
                    if (match == None):
                        item['industry_url'] = '-'
                    else:
                        item['industry_url'] = match.group(1)
                    item['industry_class_1'] = my_item4
                    item['industry_class_2'] = my_item5
                    yield item

        #下面行业内容
        cases_list1 = response.xpath('.//*[@id="main"]/div/div[1]/div/dl')
        for case1 in cases_list1:
            my_item1 = case1.xpath('.//dt/text()').extract()[0]
            if my_item1 == '所有行业':
                continue
            cases_list2 = case1.xpath('./div/ul/li')

            for case2 in cases_list2:
                my_item2 = case2.xpath('.//h4/text()').extract()[0]
                cases_list3 = case2.xpath('./div/a')

                for case3 in cases_list3:
                    item['industry_name'] = case3.xpath('.//text()').extract()[0]
                    industry_url_str = case3.xpath('.//@href').extract()[0]
                    match = re.search(r'-(.*)/', industry_url_str)
                    if (match == None):
                        item['industry_url'] = '-'
                    else:
                        item['industry_url'] = match.group(1)
                    item['industry_class_1'] = my_item1
                    item['industry_class_2'] = my_item2
                    yield item









