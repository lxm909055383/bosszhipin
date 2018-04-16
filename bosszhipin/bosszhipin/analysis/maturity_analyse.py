from bosszhipin.model.mysql_db import *
import numpy as np
import matplotlib.pyplot as plt

'''数据分析、机器学习、人工智能相关职位公司成熟度情况'''

Post = bosszhipin_post_info
mydata = Post.select(Post.financing, fn.COUNT(Post.id).alias('num')).where(Post.post_name % '%数据%'| Post.post_name % '%机器学习%'| Post.post_name % '%人工智能%').group_by(Post.financing)

labels = ['初创型', '成长型', '成熟型', '上市公司', '融资情况未知']
number = [0]*len(labels)
for item in mydata:
    if item.financing in ['不需要融资', '未融资', '天使轮']:
        number[0] += item.num
    elif item.financing in ['A轮', 'B轮']:
        number[1] += item.num
    elif item.financing in ['C轮', 'D轮及以上']:
        number[2] += item.num
    elif item.financing == '已上市':
        number[3] = item.num
    else:
        number[4] = item.num
print(number)

plt.figure(1, figsize=(5, 6))
plt.pie(number, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=True, startangle=90) #startangle表示饼图的起始角度
plt.axis('equal')
plt.title('大数据职位工作各类公司 分布', bbox={'facecolor':'0.9', 'pad':6})
# plt.legend(labels, loc='upper right', bbox_to_anchor=(1.1, 1))
plt.show()
