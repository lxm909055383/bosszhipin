from bosszhipin.model.mysql_db import *
import numpy as np
import matplotlib.pyplot as plt
import re

#分析同职位不同城市的薪资对比
Post = bosszhipin_post_info
mydata = Post.select(Post.city, Post.salary, fn.COUNT(Post.id).alias('num')).where(Post.post_name % '%数据%'| Post.post_name % '%机器学习%'| Post.post_name % '%人工智能%').group_by(Post.city, Post.salary)
Number = len(mydata)   #记录的总个数
CityList = ['北京', '上海', '广州', '深圳', '杭州', '天津', '西安', '苏州', '武汉', '厦门', '长沙', '成都']
range_1 = [0]*len(CityList)  #0k—5k（包含5）
range_2 = [0]*len(CityList)  #5k—10k（包含10）
range_3 = [0]*len(CityList)  #10k—15k（包含15）
range_4 = [0]*len(CityList)  #15k—20k（包含20）
range_5 = [0]*len(CityList)  #20k以上
for item in mydata:
    if item.city in CityList:
        m = re.match(r'(.*)K-(.*)K', item.salary)
        MinSalaryNum = int(m.group(1))
        MaxSalaryNum = int(m.group(2))
        AveSalary = (MinSalaryNum + MaxSalaryNum) / 2
        dex = CityList.index(item.city)
        if AveSalary > 0 and AveSalary <= 5:
            range_1[dex] += item.num
        elif AveSalary > 5 and AveSalary <= 10:
            range_2[dex] += item.num
        elif AveSalary > 10 and AveSalary <= 15:
            range_3[dex] += item.num
        elif AveSalary > 15 and AveSalary <= 20:
            range_4[dex] += item.num
        else:
            range_5[dex] += item.num

#绘制柱状图
N = len(CityList)
index = np.arange(N)
total_width, n = 0.8, 5
bar_width = total_width / n
index = index - (total_width - bar_width) / 2

plt.bar(index, range_1, width=bar_width, label='0k-5k')
plt.bar(index + bar_width, range_2, width=bar_width, label='5k-10k')
plt.bar(index + 2*bar_width, range_3, width=bar_width, label='10k-15k')
plt.bar(index + 3*bar_width, range_4, width=bar_width, label='15k-20k')
plt.bar(index + 4*bar_width, range_5, width=bar_width, label=u'20k以上')
#设置x轴坐标文本
plt.xticks(index + 2*bar_width, CityList)  #前面参数控制文本显示位置
# 添加数据标签
for a, b in zip(index, range_1):
    if b != 0:
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
for a, b in zip(index + bar_width, range_2):
    if b != 0:
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
for a, b in zip(index + 2*bar_width, range_3):
    if b != 0:
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
for a, b in zip(index + 3*bar_width, range_4):
    if b != 0:
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
for a, b in zip(index + 4*bar_width, range_5):
    if b != 0:
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
#x、y轴标签与图形标题
# plt.xlabel(u'城市')
# plt.ylabel(u'数量')
plt.title(u'同职位不同城市的薪资对比')
#添加图例
plt.legend()
plt.show()