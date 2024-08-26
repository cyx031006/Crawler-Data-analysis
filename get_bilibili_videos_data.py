#-*- codeing = utf-8 -*- 
#@Time : 2024/6/28 21:36
#@Author : pure81
#@Software: PyCharm

#爬取red的相关视频进行分析

import requests
# from lxml import etree
from bs4 import BeautifulSoup
import time
import random
import csv
import pandas as pd
import re
import json
def get_target(keyword, page,saveName):
    result = pd.DataFrame()

    for i in range(1, page + 1):
        headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}

        #url = 'https://search.bilibili.com/all?keyword={}&from_source=nav_suggest_new0&page={}'.format(keyword, i)
        url = 'https://search.bilibili.com/all?keyword={}&page={}&o={}'.format(keyword, i, (i-1)*30)
        html = requests.get(url.format(i), headers=headers)
        #bs = etree.HTML(html.text)
        bs = BeautifulSoup(html.content, 'html.parser')
        # items = bs.xpath('//li[@class = "video-item matrix"]')
        items = bs.find_all('div', class_='video-list-item col_3 col_xs_1_5 col_md_2 col_xl_1_7 mb_x40')
        for item in items:
            # video_url = item.xpath('div[@class = "info"]/div/a/@href')[0].replace("//","")                   #每个视频的来源地址
            # title = item.xpath('div[@class = "info"]/div/a/@title')[0]                  #每个视频的标题
            # region = item.xpath('div[@class = "info"]/div[1]/span[1]/text()')[0].strip('\n        ')          #每个视频的分类版块如动画
            # view_num = item.xpath('div[@class = "info"]/div[3]/span[1]/text()')[0].strip('\n        ')         #每个视频的播放量
            # danmu = item.xpath('div[@class = "info"]/div[3]/span[2]/text()')[0].strip('\n        ')         #弹幕
            # upload_time  = item.xpath('div[@class = "info"]/div[3]/span[3]/text()')[0].strip('\n        ')  # 上传日期
            # up_author = item.xpath('div[@class = "info"]/div[3]/span[4]/a/text()')[0].strip('\n        ')          #up主

            video_url = item.find('a')['href'].replace("//","") # 每个视频的来源地址
            title = item.find('h3', class_='bili-video-card__info--tit')['title'] # 每个视频的标题
            region = '未知'  # 每个视频的分类版块如动画
            # 根据bv号，获取具体的播放量，需要调用查看详情的api
            detail_html = requests.get('http://'+video_url,headers=headers)
            print(detail_html)
            detail_bs = BeautifulSoup(detail_html.content,'html.parser')
            with open("pure.txt",'r') as f:
                f.write(detail_html.content)
            # match = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', detail_html, re.DOTALL)  
            # if match:  
            #     # 将匹配到的字符串（JavaScript对象）转换为Python字典  
            #     initial_state = json.loads(match.group(1))  
                
            #     # 从字典中获取'videoData'下的'stat'字典，再从中获取'view'的值  
            #     view_count = initial_state.get('videoData', {}).get('stat', {}).get('view', '未找到view字段')  
            #     print(view_count)  
            # else:  
            #     print("未找到window.__INITIAL_STATE__")
            view_num = item.find_all('span', class_='bili-video-card__stats--item')[0].find('span').text # 每个视频的播放量

            danmu = item.find_all('span', class_='bili-video-card__stats--item')[1].find('span').text # 弹幕
            upload_time = item.find('span', class_='bili-video-card__info--date').text.replace(" · ","")  # 上传日期
            up_author = item.find('span', class_='bili-video-card__info--author').text  # up主

            df = pd.DataFrame({'region': [region],'title': [title], 'view_num': [view_num], 'danmu': [danmu], 'upload_time': [upload_time], 'up_author': [up_author], 'video_url': [video_url]})
            result = pd.concat([result, df])

        time.sleep(random.random() + 1)
        print('已经完成b站第 {} 页爬取'.format(i))
    saveName = saveName + ".csv"
    # result.to_csv(saveName, encoding='utf-8-sig',index=False)  # 保存为csv格式的文件
    return result

if __name__ == "__main__":
    keyword = input("请输入要搜索的关键词：")
    page = int(input("请输入要爬取的页数："))
    saveName = input("请输入要保存的文件名：")
    get_target(keyword, page,saveName)

