import pandas as pd
from pyecharts.charts import WordCloud
from pyecharts import options as opts

# 指定列名
column_names = ['SerialNumber', 'Content', 'Frequency']

# 步骤2：读取CSV文件，并指定列名
df = pd.read_csv('output/2024-07-21-fc.csv', header=None, names=column_names)

# 步骤3：筛选前80条数据
top80 = df.iloc[0:80]

# 步骤4：生成词云数据
# 确保频率列中的数据是有效的整数
word_freq = []
for index, row in top80.iterrows():
    content, frequency = row['Content'], str(row['Frequency'])  # 将频率转换为字符串
    if frequency.isdigit():  # 检查字符串是否只包含数字
        word_freq.append((content, int(frequency)))  # 添加到词云数据列表

# 步骤5：使用pyecharts生成词云图
wordcloud = (
    WordCloud()
    .add("", word_freq, word_size_range=[20, 100], shape='circle')
    .set_global_opts(title_opts=opts.TitleOpts(title="Word Cloud"))
)

# 步骤6：渲染和保存词云图
wordcloud.render('wordcloud.html')  # 保存为HTML文件