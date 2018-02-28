#!/usr/bin/python
#coding:utf-8

from scrapy import Request
from scrapy.spiders import Spider
from bosszhipin.items import BosszhipinItem
import datetime
from time import sleep
import hashlib
from bosszhipin.model.mysql_db import *


class BosszhipinSpider(Spider):
    name = 'bosszhipin'
    # 通过这个默认设置，可以不用在setting文件中设置ITEM_PIPELINES
    custom_settings = {
        'ITEM_PIPELINES': {'bosszhipin.pipelines.BosszhipinPipeline': 700}
    }

    def start_requests(self):
        #城市+行业组合（http://www.zhipin.com/c101010100-p170102）
        str_1 = 'https://www.zhipin.com/'
        str_2 = bosszhipin_city_info.select().where(bosszhipin_city_info.type == 1)   #所有包含城市的记录
        str_3 = '-'
        str_4 = bosszhipin_industry_info.select()  # 所有包含行业的记录

        #断点后提取之前已经爬取到的城市id
        city_id = int(open('city.txt', 'r').read())
        # 断点后提取之前已经爬取到的行业id
        industry_id = int(open('industry.txt', 'r').read())

        for i in str_2:    #按顺序提取城市
            if i.id < city_id:
                continue
            #将当前调取城市的id写入文件
            with open("city.txt", "w") as f1:
                f1.write(str(i.id))

            for j in str_4:     #按顺序提取行业
                if j.id <= industry_id:
                    continue
                # 将当前调取行业的id写入文件
                with open("industry.txt", "w") as f2:
                    f2.write(str(j.id))

                #更新城市调用次数
                p = bosszhipin_city_info.update(use_times=bosszhipin_city_info.use_times + 1).where(bosszhipin_city_info.name == i.name)
                p.execute()
                #更新行业调用次数
                q = bosszhipin_industry_info.update(use_times=bosszhipin_industry_info.use_times + 1).where(bosszhipin_industry_info.url == j.url)
                q.execute()
                url = '%s%s%s%s' % (str_1, i.url, str_3, j.url)
                yield Request(url)
            #行业调取完一遍后重置为1
            with open("industry.txt", "w") as f2:
                f2.write('0')
        with open("city.txt", "w") as f1:
            f1.write('1')

        # #城市+行业+区组合（http://www.zhipin.com/c101200100-p110101/b_洪山区）
        # str_1 = 'https://www.zhipin.com/'
        # str_2 = bosszhipin_city_info.select().where(bosszhipin_city_info.type == 1)   #所有包含城市的记录
        # str_3 = '-'
        # str_4 = bosszhipin_industry_info.select()  # 所有包含行业的记录
        # str_5 = '/b_'
        # str_6 = bosszhipin_city_info.select().where(bosszhipin_city_info.type == 2)    #所有包含区域的记录
        # for i in str_2:    #按顺序提取城市
        #     for j in str_4:    #按顺序提取行业
        #         for k in str_6:  # 按顺序提取区域
        #             #更新城市调用次数
        #             p = bosszhipin_city_info.update(use_times=bosszhipin_city_info.use_times + 1).where(bosszhipin_city_info.name == i.name)
        #             p.execute()
        #             #更新行业调用次数
        #             q = bosszhipin_industry_info.update(use_times=bosszhipin_industry_info.use_times + 1).where(bosszhipin_industry_info.url == j.url)
        #             q.execute()
        #             # 更新区域调用次数
        #             r = bosszhipin_city_info.update(use_times=bosszhipin_city_info.use_times + 1).where(bosszhipin_city_info.name == k.name, bosszhipin_city_info.url == i.url)
        #             r.execute()
        #             url = '%s%s%s%s%s%s' % (str_1, i.url, str_3, j.url, str_5, k.name)
        #             yield Request(url)

    # #改版之前
    # def parse(self, response):
    #     item = BosszhipinItem()
    #     cases = response.xpath('//div[@class="job-list"]/ul/li')
    #     for case in cases:
    #         item['Job'] = case.xpath('.//div[@class="info-primary"]/h3/a/text()').extract()[0]
    #         item['Salary'] = case.xpath('.//div[@class="info-primary"]/h3/a/span/text()').extract()[0]
    #         item['Company'] = case.xpath('.//div[@class="company-text"]/h3/a/text()').extract()[0]
    #         item['City'] = case.xpath('.//div[@class="info-primary"]/p/text()[1]').extract()[0]
    #         item['Experience'] = case.xpath('.//div[@class="info-primary"]/p/text()[2]').extract()[0]
    #         item['Education'] = case.xpath('.//div[@class="info-primary"]/p/text()[3]').extract()[0]
    #         item['Industry'] = case.xpath('.//div[@class="company-text"]/p/text()[1]').extract()[0]
    #         str1 = case.xpath('.//div[@class="company-text"]/p/text()[2]').extract()[0]
    #         if u'\u4eba' in str1:
    #             item['Financing'] = '融资情况未知'
    #             item['CompanySize'] = case.xpath('.//div[@class="company-text"]/p/text()[2]').extract()[0]
    #         else:
    #             item['Financing'] = str1
    #             item['CompanySize'] = case.xpath('.//div[@class="company-text"]/p/text()[3]').extract()[0]
    #
    #         data = case.xpath('.//div[@class="job-tags"]/span')
    #         data_text = ','.join(data.xpath('string(.)').extract())
    #         if u'\u53d1\u5e03' in data_text:
    #             item['KeyWord'] = '关键字未知'
    #             Pub_Time = data_text
    #         else:
    #             item['KeyWord'] = data_text
    #             Pub_Time = case.xpath('.//div[@class="job-time"]/span/text()').extract()
    #
    #         #上面的Pub_Time是一个列表，所需元素在第一个
    #         #处理今天、时间（默认是今天）、昨天
    #         today = datetime.date.today()
    #         if u'\u4eca\u5929' in Pub_Time[0]:      #unicode编码今天
    #             item['PubTime'] = str(today)
    #         elif ':' in Pub_Time[0]:                 #时间
    #             item['PubTime'] = str(today)
    #         elif u'\u6628\u5929' in Pub_Time[0]:    # unicode编码昨天
    #             item['PubTime'] = str(today - datetime.timedelta(days=1))
    #         #处理2018和2017年
    #         else:
    #             if u'\u0030\u0031\u6708' in Pub_Time[0]:      #01月说明是2018年
    #                 newstr = str(datetime.datetime.now().year) + u'\u5e74' + Pub_Time[0][3:]
    #             else:
    #                 newstr = str(datetime.datetime.now().year - 1) + u'\u5e74' + Pub_Time[0][3:]
    #             # 日期变换成****-**-**形式（因为前面datetime转化的形式是这样，得统一）
    #             item['PubTime'] = newstr.replace(u'\u5e74', '-').replace(u'\u6708', '-').replace(u'\u65e5', '')
    #
    #         item['ContactPerson'] = case.xpath('.//div[@class="job-author"]/p/text()[1]').extract()[0]
    #         item['Duties'] = case.xpath('.//div[@class="job-author"]/p/text()[2]').extract()[0]
    #         item['Img'] = case.xpath('.//div[@class="job-author"]/p/img/@src').extract()[0]
    #
    #         #通过几个字段组合为md5值
    #         Md5_str = '%s%s%s%s%s%s%s%s' % (item['Job'], item['Salary'], item['Company'], item['City'], item['Experience'], item['Education'], item['ContactPerson'], item['PubTime'])
    #         m = hashlib.md5()
    #         try:
    #             m.update(Md5_str.encode(encoding='gb2312'))    #以后尽量不用这种编码
    #         except:
    #             continue
    #         item['Md5'] = m.hexdigest()
    #
    #         yield item
    #     sleep(1.3)

    #改版之后
    def parse(self, response):
        cases = response.xpath('//*[@id="main"]/div/div[2]/ul/li')
        for case in cases:
            item = BosszhipinItem()   #必须放到循环里面，不然都会重复一个
            item['Job'] = case.xpath('.//div/div[1]/h3/a/div[1]/text()').extract()[0]
            item['Salary'] = case.xpath('.//div/div[1]/h3/a/span/text()').extract()[0]
            item['Company'] = case.xpath('.//div/div[2]/div/h3/a/text()').extract()[0]
            item['Experience'] = case.xpath('.//div/div[1]/p/text()[2]').extract()[0]
            item['Education'] = case.xpath('.//div/div[1]/p/text()[3]').extract()[0]

            #Industry，Financing，CompanySize在一个数组里面
            item['Industry'] = case.xpath('.//div/div[2]/div/p/text()[1]').extract()[0]
            str1 = case.xpath('.//div[@class="company-text"]/p/text()[2]').extract()[0]
            if u'\u4eba' in str1:
                item['Financing'] = '融资情况未知'
                item['CompanySize'] = case.xpath('.//div[@class="company-text"]/p/text()[2]').extract()[0]
            else:
                item['Financing'] = str1
                item['CompanySize'] = case.xpath('.//div[@class="company-text"]/p/text()[3]').extract()[0]

            # 下面的Pub_Time是一个列表，所需元素在第一个
            Pub_Time = case.xpath('.//div/div[3]/p/text()').extract()
            # 处理今天、时间（默认是今天）、昨天
            today = datetime.date.today()
            if u'\u4eca\u5929' in Pub_Time[0]:  # unicode编码今天
                item['PubTime'] = str(today)
            elif ':' in Pub_Time[0]:  # 时间
                item['PubTime'] = str(today)
            elif u'\u6628\u5929' in Pub_Time[0]:  # unicode编码昨天
                item['PubTime'] = str(today - datetime.timedelta(days=1))
            # 处理2018和2017年
            else:
                if u'\u0030\u0031\u6708' in Pub_Time[0]:  # 01月说明是2018年
                    newstr = str(datetime.datetime.now().year) + u'\u5e74' + Pub_Time[0][3:]
                else:
                    newstr = str(datetime.datetime.now().year - 1) + u'\u5e74' + Pub_Time[0][3:]
                # 日期变换成****-**-**形式（因为前面datetime转化的形式是这样，得统一）
                item['PubTime'] = newstr.replace(u'\u5e74', '-').replace(u'\u6708', '-').replace(u'\u65e5', '')

            #联系人信息
            item['ContactPerson'] = case.xpath('.//div/div[3]/h3/text()[1]').extract()[0]
            item['Duties'] = case.xpath('.//div/div[3]/h3/text()[2]').extract()[0]
            item['Img'] = case.xpath('.//div/div[3]/h3/img/@src').extract()[0]

            #链接到落地页
            link_url = 'https://www.zhipin.com' + case.xpath('.//div/div[1]/h3/a/@href').extract()[0]
            if link_url:
                yield Request(link_url, meta={'key': item}, callback=self.parse_info)

    def parse_info(self, response):
        item = response.meta['key']
        #关键词
        try:
            data = response.xpath('.//*[@id="main"]/div[1]/div/div/div[2]/div[3]/span')
            item['KeyWord'] = ','.join(data.xpath('string(.)').extract())
        except:
            item['KeyWord'] = '关键字未知'

        #城市
        item['City'] = response.xpath('.//*[@id="main"]/div[1]/div/div/div[2]/p/text()[1]').extract()[0]

        # 通过几个字段组合为md5值
        Md5_str = '%s%s%s%s%s%s%s%s' % (item['Job'], item['Salary'], item['Company'], item['City'], item['Experience'], item['Education'], item['ContactPerson'], item['PubTime'])
        m = hashlib.md5()
        try:
            m.update(Md5_str.encode(encoding='gb2312'))  # 以后尽量不用这种编码
            item['Md5'] = m.hexdigest()
        except:
            item['Md5'] = '编码出错'
        yield item

        # #爬取后面的网页（改版之前）
        # next_url = response.xpath('//*[@id="main"]/div[3]/div[2]/div[2]/a[@ka="page-next"]/@href').extract()
        # if 'page' in next_url[0]:
        #     next_url = 'https://www.zhipin.com' + next_url[0]
        #     print(111111111111)
        #     print(next_url)
        #     print(222222222222)
        #     yield Request(next_url)

        # # 爬取后面的网页（改版之后）  有错误！！！！！！！！！！！！
        # next_url = response.xpath('//*[@id="main"]/div/div[2]/div[2]/a[@ka="page-next"]/@href').extract()
        # print(111111111111)
        # print(next_url)
        # print(222222222222)
        # print(next_url[0])
        #
        # if 'page' in next_url[0]:
        #     next_url = 'https://www.zhipin.com' + next_url
        #     print(111111111111)
        #     print(next_url)
        #     print(222222222222)
        #     yield Request(next_url)
