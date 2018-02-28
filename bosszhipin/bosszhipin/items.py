# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#城市信息item
class CityInfoItem(scrapy.Item):
    city_name = scrapy.Field()
    city_url = scrapy.Field()
    city_type = scrapy.Field()
    pass


#行业信息item
class IndustryInfoItem(scrapy.Item):
    industry_name = scrapy.Field()
    industry_url = scrapy.Field()
    industry_class_1 = scrapy.Field()
    industry_class_2 = scrapy.Field()
    pass


#招聘信息item
class BosszhipinItem(scrapy.Item):
    Job = scrapy.Field()
    Salary = scrapy.Field()
    Company = scrapy.Field()
    City = scrapy.Field()
    Experience = scrapy.Field()
    Education = scrapy.Field()
    CompanySize = scrapy.Field()
    Financing = scrapy.Field()
    Industry = scrapy.Field()
    KeyWord = scrapy.Field()
    ContactPerson = scrapy.Field()
    Duties = scrapy.Field()
    Img = scrapy.Field()
    PubTime = scrapy.Field()
    Md5 = scrapy.Field()

    pass





