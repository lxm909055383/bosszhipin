from bosszhipin.model.mysql_db import *
from datetime import datetime

#城市信息Pipline
class CityInfoPipeline(object):
    def process_item(self, item, spider):
        #继承bosszhipin_city_info类
        model = bosszhipin_city_info()
        #name、url、type三个字段直接爬取得到
        model.name = item['city_name']
        model.url = item['city_url']
        model.type = item['city_type']
        #father_id字段通过url、type来确定
        try:
            st = bosszhipin_city_info.select().where(bosszhipin_city_info.url == model.url, bosszhipin_city_info.type == 1).get()  #get方法只会返回一条记录
        except:
            model.father_id = -1
        else:
            model.father_id = st.id
        #created_at、updated_at字段
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        model.created_at = now
        model.updated_at = now
        #更新updated_at字段
        q = bosszhipin_city_info.update(updated_at=now).where(bosszhipin_city_info.name == model.name, bosszhipin_city_info.url == model.url)
        q.execute()
        #根据name、url达到去重目的
        try:
            bosszhipin_city_info.get(bosszhipin_city_info.name == model.name, bosszhipin_city_info.url == model.url)   #若数据库里没有同名同url同时间的记录，就会报错异常执行except保存
        except:
            model.save()


# 行业信息Pipline
class IndustryInfoPipeline(object):
    def process_item(self, item, spider):
        # 继承bosszhipin_industry_info类
        model = bosszhipin_industry_info()
        # name、url、class_2、class_1字段直接爬取得到
        model.name = item['industry_name']
        model.url = item['industry_url']
        model.class_2 = item['industry_class_2']
        model.class_1 = item['industry_class_1']
        # created_at、updated_at字段
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        model.created_at = now
        model.updated_at = now
        # 更新updated_at字段
        q = bosszhipin_industry_info.update(updated_at=now).where(bosszhipin_industry_info.name == model.name, bosszhipin_industry_info.url == model.url)
        q.execute()
        # 根据name、url达到去重目的
        try:
            bosszhipin_industry_info.get(bosszhipin_industry_info.name == model.name, bosszhipin_industry_info.url == model.url)
        except:
            model.save()


#招聘信息Pipline
class BosszhipinPipeline(object):
    def process_item(self, item, spider):
        # 继承bosszhipin_post_info类
        model = bosszhipin_post_info()
        # 直接爬取得到的字段
        model.md5 = item['Md5']
        model.post_name = item['Job']
        model.salary = item['Salary']
        model.company = item['Company']
        model.city = item['City']
        model.industry = item['Industry']
        model.financing = item['Financing']
        model.company_size = item['CompanySize']
        model.key_word = item['KeyWord']
        model.experience = item['Experience']
        model.education = item['Education']
        model.contact_name = item['ContactPerson']
        model.contact_duties = item['Duties']
        model.contact_photo = item['Img']
        model.publish_time = item['PubTime']

        # created_at、updated_at字段
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        model.created_at = now
        model.updated_at = now
        # 更新updated_at字段
        q = bosszhipin_post_info.update(updated_at=now).where(bosszhipin_post_info.md5 == model.md5, bosszhipin_post_info.publish_time == model.publish_time)
        q.execute()
        # 根据md5和publish_time达到去重目的
        try:
            bosszhipin_post_info.get(bosszhipin_post_info.md5 == model.md5, bosszhipin_post_info.publish_time == model.publish_time)
        except:
            model.save()
