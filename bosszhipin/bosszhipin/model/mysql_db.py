
from peewee import *

# db = MySQLDatabase(database='bosszhipin', host='localhost', password='Lxm941202mysql', port=3306, user='root')
db = MySQLDatabase(database='bosszhipin', host='localhost', password='passw0rd', port=3306, user='root')
# db = MySQLDatabase(database='bosszhipin', host='127.0.0.1', password='', port=3306, user='root')

# 城市信息入库信息
class bosszhipin_city_info(Model):
    father_id = IntegerField(default=-1)   #IntegerField不能设置最大长度
    type = IntegerField(default=0)
    name = CharField(max_length=32, default='null')
    url = CharField(max_length=64, default='null')
    use_times = IntegerField(default=0)
    created_at = DateTimeField(default='0000-00-00 00:00:00')
    updated_at = DateTimeField(default='0000-00-00 00:00:00')
    class Meta:
        database = db

# 行业信息入库信息
class bosszhipin_industry_info(Model):
    name = CharField(max_length=32, default='null', index=True)
    url = CharField(max_length=64, default='null')
    class_1 = CharField(max_length=32, default='null')
    class_2 = CharField(max_length=32, default='null')
    use_times = IntegerField(default=0)
    created_at = DateTimeField(default='0000-00-00 00:00:00')
    updated_at = DateTimeField(default='0000-00-00 00:00:00')
    class Meta:
        database = db

#招聘信息入库信息
class bosszhipin_post_info(Model):
    md5 = CharField(max_length=32, default='null', index=True)
    post_name = CharField(max_length=32, default='null', index=True)
    salary = CharField(max_length=32, default='null')
    company = CharField(max_length=32, default='null', index=True)
    city = CharField(max_length=32, default='null', index=True)
    industry = CharField(max_length=32, default='null', index=True)
    financing = CharField(max_length=32, default='null')
    company_size = CharField(max_length=32, default='null')
    key_word = CharField(max_length=32, default='null')
    experience = CharField(max_length=32, default='null')
    education = CharField(max_length=32, default='null')
    contact_name = CharField(max_length=32, default='null')
    contact_duties = CharField(max_length=32, default='null')
    contact_photo = CharField(max_length=256, default='null')
    publish_time = CharField(max_length=32, default='null')
    created_at = DateTimeField(default='0000-00-00 00:00:00')
    updated_at = DateTimeField(default='0000-00-00 00:00:00')
    class Meta:
        database = db

#连接数据库
db.connect()
#创建表时如果表已存在会报错，捕获异常直接跳过
try:
    db.create_tables([bosszhipin_city_info, bosszhipin_industry_info, bosszhipin_post_info])
except:
    pass
