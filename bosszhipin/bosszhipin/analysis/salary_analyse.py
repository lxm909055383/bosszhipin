from bosszhipin.model.mysql_db import *
import numpy as np
import matplotlib.pyplot as plt
from pyecharts import Pie
import os
import re

'''数据分析、机器学习、人工智能相关职位薪资分布'''

html_path = './html_dir/'
if not os.path.exists(html_path):
    os.makedirs(html_path)

Post = bosszhipin_post_info
mydata = Post.select(Post.salary, fn.COUNT(Post.id).alias('num')).where(Post.post_name % '%数据%'| Post.post_name % '%机器学习%'| Post.post_name % '%人工智能%').group_by(Post.salary)

labels = ['0k-5k', '5k-10k', '10k-15k', '15k-20k', '20k以上']
number = [0]*len(labels)
for item in mydata:
    m = re.match(r'(.*)K-(.*)K', item.salary)
    MinSalaryNum = int(m.group(1))
    MaxSalaryNum = int(m.group(2))
    AveSalary = (MinSalaryNum + MaxSalaryNum) / 2
    if AveSalary > 0 and AveSalary <= 5:
        number[0] += item.num
    elif AveSalary > 5 and AveSalary <= 10:
        number[1] += item.num
    elif AveSalary > 10 and AveSalary <= 15:
        number[2] += item.num
    elif AveSalary > 15 and AveSalary <= 20:
        number[3] += item.num
    else:
        number[4] += item.num
print(number)

pie = Pie('大数据职位薪资分布', title_text_size=25, title_pos="center", width=800, height=500)
pie.add("", labels, number, is_label_show=True, label_text_size=15, legend_text_size=15, legend_orient='vertical',
        legend_pos='right', levisual_text_color="#fff", symbol_size=10)
pie.show_config()
pie.render(f'{html_path}salary.html')


# plt.figure(1, figsize=(5, 6))
# plt.pie(number, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=True, startangle=90) #startangle表示饼图的起始角度
# plt.axis('equal')
# plt.title('大数据职位工作各类公司 分布', bbox={'facecolor':'0.9', 'pad':6})
# # plt.legend(labels, loc='upper right', bbox_to_anchor=(1.1, 1))
# plt.show()
