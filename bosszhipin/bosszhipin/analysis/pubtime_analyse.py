from bosszhipin.model.mysql_db import *
import numpy as np
import matplotlib.pyplot as plt
from pyecharts import Line
import os

'''数据分析、机器学习、人工智能相关职位一个月内发布情况'''

html_path = './html_dir/'
if not os.path.exists(html_path):
    os.makedirs(html_path)

Post = bosszhipin_post_info
mydata = Post.select(Post.publish_time, fn.COUNT(Post.id).alias('num')).where(Post.post_name % '%数据%'| Post.post_name % '%机器学习%'| Post.post_name % '%人工智能%').group_by(Post.publish_time).having(Post.publish_time >= '2017-12-01', Post.publish_time <= '2018-01-31').order_by(Post.publish_time)

labels_1 = []
number_1 = []
labels_2 = []
number_2 = []
for item in mydata:
    if item.publish_time >= '2017-12-01' and item.publish_time <= '2017-12-31':
        labels_1.append(item.publish_time)
        number_1.append(item.num)
    else:
        labels_2.append(item.publish_time)
        number_2.append(item.num)
# print(labels_1)
# print(number_1)
# print(labels_2)
# print(number_2)

line = Line('大数据职位一个月内发布情况', title_text_size=25, title_pos="center", width=800, height=500)
line.add("2017年12月", labels_1, number_1, is_label_show=True, label_text_size=15, legend_text_size=15, legend_orient='vertical', legend_pos='right', levisual_text_color="#fff")
line.add("2018年1月", labels_2, number_2, is_label_show=True, label_text_size=15, legend_text_size=15, legend_orient='vertical', legend_pos='right', levisual_text_color="#fff")
line.show_config()
line.render(f'{html_path}pubtime.html')
