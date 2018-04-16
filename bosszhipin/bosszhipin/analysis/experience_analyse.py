from bosszhipin.model.mysql_db import *
import numpy as np
import matplotlib.pyplot as plt

'''数据分析、机器学习、人工智能相关职位对工作年限的要求'''

Post = bosszhipin_post_info
mydata = Post.select(Post.experience, fn.COUNT(Post.id).alias('num')).where(Post.post_name % '%数据%'| Post.post_name % '%机器学习%'| Post.post_name % '%人工智能%').group_by(Post.experience)

labels = ['经验不限', '应届生', '1年以内', '1-3年', '3-5年', '5-10年', '10年以上']
number = [0]*len(labels)
for item in mydata:
        dex = labels.index(item.experience)
        number[dex] = item.num
print(number)
plt.figure(1, figsize=(5, 6))
plt.pie(number, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=True, startangle=90) #startangle表示饼图的起始角度
plt.axis('equal')
plt.title('大数据职位工作年限要求', bbox={'facecolor':'0.9', 'pad':6})
# plt.legend(labels, loc='upper right', bbox_to_anchor=(1.1, 1))
plt.show()
