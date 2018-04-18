from bosszhipin.model.mysql_db import *
import numpy as np
import matplotlib.pyplot as plt
from pyecharts import Bar
from pyecharts import Pie
import os

'''数据分析、机器学习、人工智能相关职位在各大城市的分布'''

html_path = './html_dir/'
if not os.path.exists(html_path):
    os.makedirs(html_path)

Post = bosszhipin_post_info
mydata = Post.select(Post.city, fn.COUNT(Post.id).alias('num')).where(Post.post_name % '%数据%'| Post.post_name % '%机器学习%'| Post.post_name % '%人工智能%').group_by(Post.city)
labels = ['北京', '上海', '广州', '深圳', '杭州', '天津', '西安', '苏州', '武汉', '厦门', '长沙', '成都']
number = [0]*len(labels)
for item in mydata:
    if item.city in labels:
        dex = labels.index(item.city)
        number[dex] = item.num
print(number)

#柱状图
bar = Bar('大数据职位在各大城市的分布', title_text_size=25, title_pos="center", width=800, height=500)
bar.add("", labels, number, is_random=True, xaxis_label_textsize=20, yaxis_label_textsize=20, is_label_show=True, label_text_size=15, legend_text_size=15, legend_orient='vertical',legend_pos='right', levisual_text_color="#fff", symbol_size=15)
bar.show_config()
bar.render(f'{html_path}city_bar.html')

#饼图
pie = Pie('大数据职位在各大城市的分布', title_text_size=25, title_pos="center", width=800, height=500)
pie.add("", labels, number, is_label_show=True, label_text_size=15, legend_text_size=15, legend_orient='vertical',legend_pos='right', levisual_text_color="#fff", symbol_size=15)
pie.show_config()
pie.render(f'{html_path}city_pie.html')


