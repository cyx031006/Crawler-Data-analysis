# coding=utf-8
import time
import jieba
import re
from collections import Counter

def get_word_frequency():

    # 停用词文件路径
    stopwords_path = 'cn_stopwords.txt'

    # 读取停用词
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        stop_words = set([line.strip() for line in f])

    #------------------------------------中文分词------------------------------------
    # Output file for segmented words
    output_file = 'output/C-class-fenci.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        # Input file
        input_file = 'output/clean弹幕内容.txt'
        for line in open(input_file, encoding='utf-8'):
            line = line.strip('\n')  # Ensure line.strip() affects line
            seg_list = jieba.cut(line, cut_all=False)
            # 过滤掉停用词
            seg_list_filtered = [word for word in seg_list if word not in stop_words]
            cut_words = " ".join(seg_list_filtered)
            f.write(cut_words + "\n")  # Ensure each line is written separately

    # 为了词频统计，我们需要把所有分词结果合并在一起
    with open(output_file, 'r', encoding='utf-8') as f:
        all_words = f.read().split()

    # 输出结果
    print(all_words)

    # 词频统计
    c = Counter()
    for x in all_words:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1

    # 输出词频最高的前10个词
    print('\n词频统计结果：')
    for (k, v) in c.most_common(10):
        print("%s:%d" % (k, v))

    # 存储数据
    name = time.strftime("%Y-%m-%d") + "-fc.csv"
    with open("output/"+name, 'w', encoding='utf-8') as fw:
        i = 1
        for (k, v) in c.most_common(len(c)):
            fw.write(str(i) + ',' + str(k) + ',' + str(v) + '\n')
            i = i + 1

    print("Over write file!")