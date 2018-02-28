# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

# from scrapy import signals
#
# class BosszhipinSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


#用户代理
# import scrapy
# from scrapy import signals
# from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
# import random
#
# class MyUserAgentMiddleware(UserAgentMiddleware):
#
#     def __init__(self, user_agent):
#         self.user_agent = user_agent
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             user_agent=crawler.settings.get('MY_USER_AGENT')
#         )
#
#     def process_request(self, request, spider):
#         agent = random.choice(self.user_agent)
#         print('------')
#         print(agent)
#         print('------')
#         request.headers['User-Agent'] = agent


# -*- coding: utf-8 -*-
# 导入随机模块
import random
# 导入settings文件中的IPPOOL
from .settings import IPPOOL
# 导入官方文档对应的HttpProxyMiddleware
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware

class IPPOOlS(HttpProxyMiddleware):
    # 初始化
    def __init__(self, ip=''):
        self.ip = ip

    # 请求处理
    def process_request(self, request, spider):
        # 先随机选择一个IP
        thisip = random.choice(IPPOOL)
        print("当前使用IP是：" + thisip["ipaddr"])
        request.meta["proxy"] = "http://" + thisip["ipaddr"]