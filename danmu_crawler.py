import re
import requests
import pandas as pd
import time
from tqdm import trange
from data_cleaning import cleaning_data  # 第二步，清洗数据
from word_frequency import get_word_frequency # 第三步，获取词频
from sentiment_distribution import create_danmu_html # 第四步，生成html文件
HEADERS_TEMPLATE = {
    "origin": "https://www.bilibili.com",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"
}

# 获取弹幕URL的函数
def get_danmu_urls(oid, start, end):
    """
    获取指定日期范围内的弹幕URL列表

    oid: 视频的唯一标识符
    start: 开始日期
    end: 结束日期
    return: 弹幕URL列表
    """
    date_list = pd.date_range(start, end).strftime('%Y-%m-%d').tolist()
    url_list = [
        f"https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={oid}&date={date}"
        for date in date_list
    ]
    return url_list

# 解析弹幕文件的函数
def parse_so_file(filepath):
    """
    解析 .so 文件并提取弹幕内容

    filepath: .so文件路径
    return: 弹幕内容列表
    """
    with open(filepath, 'rb') as file:
        data = file.read()
    text = data.decode('utf-8', errors='ignore')
    danmu_list = re.findall(r':(.*?)@', text)  # 利用正则表达式提取so文件的弹幕内容
    return danmu_list

# 下载并解析弹幕的函数
def download_and_parse_danmu(url_list, headers):
    """
    下载弹幕文件并解析为文本

    url_list: 弹幕文件URL列表
    headers: HTTP请求头
    return: 所有弹幕内容的列表
    """
    danmakus = []
    for i in trange(len(url_list)):  # 显示进度条
        url = url_list[i]
        response = requests.get(url, headers=headers)
        so_filepath = "output/danmu_so/"+f"danmu_{i}.so"
        with open(so_filepath, 'wb') as so_file:
            so_file.write(response.content)
        danmu_list = parse_so_file(so_filepath)
        danmakus.extend(danmu_list)
        time.sleep(2)
    return danmakus

# 保存弹幕到文本文件的函数
def save_danmu_to_file(danmakus, filename):
    """
    将弹幕内容保存到本地文本文件

    danmakus: 弹幕内容列表
    filename: 保存文件的名称
    """
    with open(f"{filename}", 'w', encoding='utf-8') as file:
        for danmu in danmakus:
            file.write(danmu + '\n')
    print(f"{filename} 已生成")

# 主函数
def main():
    print("=" * 30)
    print("请先按照本项目最后cookie及oid获取方式获取你的cookie和对应视频oid")
    print("=" * 30)
    print("请按照下面提示输入需要爬取的弹幕时间，建议不要超过最近两个月")
    print("=" * 30)

    start = input("请输入弹幕开始时间，格式年-月-日，例2020-09-01：")
    end = input("请输入弹幕结束时间，格式年-月-日，例2020-09-20：")
    # cookie = input("请输入你的Cookie：")
    # oid = input("请输入对应视频oid：")
    oid = "500001660574785"
    # name = input("请输入保存文件名称：")
    name = "output/弹幕内容.txt"

    headers = HEADERS_TEMPLATE.copy()
    headers["cookie"] = "buvid3=D65D4B7D-A402-3C12-EEF2-0DA49AE1EC4682143infoc; b_nut=1715227882; _uuid=F5E8A886-EE19-113B-B352-2A1689BFEB3882218infoc; enable_web_push=DISABLE; home_feed_column=5; buvid4=FD71BAA8-BCF2-DF10-922F-57C534F786E082794-024050904-4ioT9isT2fxPz20sX4cuig%3D%3D; rpdid=|(um|JRY)Juk0J'u~ulkk~))R; DedeUserID=61814778; DedeUserID__ckMd5=ac5e26267ea6da24; header_theme_version=CLOSE; buvid_fp_plain=undefined; hit-dyn-v2=1; CURRENT_QUALITY=80; PVID=1; CURRENT_BLACKGAP=0; fingerprint=9409dc45be030ceff17dc72f42d03ae4; CURRENT_FNVAL=4048; buvid_fp=9409dc45be030ceff17dc72f42d03ae4; b_lsid=10EA6FF210_1918C64A00E; browser_resolution=1920-476; SESSDATA=c9b8d325%2C1740189291%2C05db3%2A82CjA4c22iUPpCCQO_iz0c3XnCMzGd8DcavaEzi4LbOs6MD97-c_9Pd7Qy4afXb6hA3ZgSVjg5WGRMeEZQVWlOY2RfUS1IT2R3SHVqSkdFTF9mWU5qN2dDRDFvQXducU9ua0t1aUtmRENYcjV3WEM1aTN1bDNMeVFUOTFVcjAwQ2l0aU9LVFVub19RIIEC; bili_jct=ffca1665fb6bd01544d6efb33099af42; bp_t_offset_61814778=969798860908003328; sid=8rq3yaro; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQ4OTY1MDIsImlhdCI6MTcyNDYzNzI0MiwicGx0IjotMX0.77JMuoMC4bWa7xbl_87FYrNM8wxjnxtuVD3TI2EAgrg; bili_ticket_expires=1724896442"
    headers["referer"] = f"https://www.bilibili.com/video/BV19z421q7GM/?spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=5ec0bdf3923f0e72967dd9c6650e7943&oid={oid}"

    print("========正在爬取弹幕=========")
    url_list = get_danmu_urls(oid, start, end)
    danmakus = download_and_parse_danmu(url_list, headers)

    print("========正在保存弹幕文本文件========")
    save_danmu_to_file(danmakus, name)
    print(name)
    return name

if __name__ == "__main__":
    file_name = main()
    clean_data_file_path =  cleaning_data(file_name)
    get_word_frequency()
    create_danmu_html()

