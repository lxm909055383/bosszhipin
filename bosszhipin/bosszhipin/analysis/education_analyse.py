from bosszhipin.model.mysql_db import *
import numpy as np
import matplotlib.pyplot as plt

'''数据分析、机器学习、人工智能相关职位对学历的要求'''

Post = bosszhipin_post_info
mydata = Post.select(Post.education, fn.COUNT(Post.id).alias('num')).where(Post.post_name % '%数据%'| Post.post_name % '%机器学习%'| Post.post_name % '%人工智能%').group_by(Post.education)

labels = ['硕士', '本科', '大专', '不限']
number = [0]*len(labels)
for item in mydata:
    if item.education == '博士' or item.education == '硕士':
        number[0] += item.num
    elif item.education not in labels:
        number[-1] += item.num
    else:
        dex = labels.index(item.education)
        number[dex] = item.num

plt.figure(1, figsize=(5, 6))
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
plt.pie(number, labels=labels, colors=colors, autopct='%1.1f%%', pctdistance=0.8, shadow=True, startangle=90) #startangle表示饼图的起始角度
plt.axis('equal')
plt.title('大数据职位学历要求', bbox={'facecolor':'0.9', 'pad':6})
# plt.legend(labels)
plt.show()
