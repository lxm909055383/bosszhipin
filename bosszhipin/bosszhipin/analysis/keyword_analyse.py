from bosszhipin.model.mysql_db import *
import matplotlib.pyplot as plt
import codecs
import jieba
from wordcloud import WordCloud
import os

wordcloud_path = './wordcloud/'
if not os.path.exists(wordcloud_path):
    os.makedirs(wordcloud_path)

#制作词云图
Post = bosszhipin_post_info
#模糊查询,并使用了OR操作
mydata_2 = Post.select(Post.key_word).where(Post.post_name % '%数据%'| Post.post_name % '%机器学习%'| Post.post_name % '%人工智能%')
#将字符串存入文件中
fr = codecs.open(f'{wordcloud_path}word_set.txt', 'a', encoding='utf8')
for item in mydata_2:
    fr.write(item.key_word)
    fr.write(',')
fr.close()
#从文件中提取字符串并进行分词
text = codecs.open(f'{wordcloud_path}word_set.txt',"r", encoding='utf8').read()
cut_text= jieba.cut(text)
result= ''.join(cut_text)
# print(result)
#找到能用的中文字体
font = r'C:\Windows\Fonts\simfang.ttf'
wc = WordCloud(collocations=False, font_path=font,background_color='white',width=800,height=600,max_font_size=100,max_words=500)#,min_font_size=10)#,mode='RGBA',colormap='pink')
wc.generate(result)
#保存图片
wc.to_file(f'{wordcloud_path}wordcloud.png')
#显示图片
plt.figure("关键词云图") #指定所绘图名称
plt.imshow(wc)       # 以图片的形式显示词云
plt.axis("off")      #关闭图像坐标系
plt.show()