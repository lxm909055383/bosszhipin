from bosszhipin.model.mysql_db import *
import numpy as np
import matplotlib.pyplot as plt


#各城市对职位的需求量（包括总的职位数与公司数）
Post = bosszhipin_post_info
mydata_2 = Post.select(Post.city, fn.COUNT(fn.Distinct(Post.company)).alias('company_num'), fn.COUNT(Post.id).alias('position_num')).group_by(Post.city)

CityList = ['北京', '上海', '广州', '深圳', '杭州', '天津', '西安', '苏州', '武汉', '厦门', '长沙', '成都']
CompanyNumList = [0]*len(CityList)
PositionNumList = [0]*len(CityList)
#将城市列表、公司数量、职位数量分别存在列表中
for item in mydata_2:
    if item.city in CityList:
        dex = CityList.index(item.city)
        CompanyNumList[dex] = item.company_num
        PositionNumList[dex] = item.position_num

#绘制柱状图
N = len(CityList)
index = np.arange(N)
total_width, n = 0.8, 2
bar_width = total_width / n
index = index - (total_width - bar_width) / 2

plt.bar(index, CompanyNumList, width=bar_width, label=u'公司数量')
plt.bar(index + bar_width, PositionNumList, width=bar_width, label=u'职位数量')
#设置x轴坐标文本
plt.xticks(index + 0.5*bar_width, CityList)  #前面参数控制文本显示位置
# 添加数据标签
for a, b in zip(index, CompanyNumList):
    if b != 0:
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
for a, b in zip(index + bar_width, PositionNumList):
    if b != 0:
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
#x、y轴标签与图形标题
# plt.xlabel(u'城市')
# plt.ylabel(u'数量')
plt.title(u'不同城市的公司数与职位数')
#添加图例
plt.legend()
plt.show()


