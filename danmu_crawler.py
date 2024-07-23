import re
import requests
import pandas as pd
import time
from tqdm import trange

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
        so_filepath = f"danmu_{i}.so"
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
    with open(f"{filename}.txt", 'w', encoding='utf-8') as file:
        for danmu in danmakus:
            file.write(danmu + '\n')
    print(f"{filename}.txt 已生成")

# 主函数
def main():
    print("=" * 30)
    print("请先按照本项目最后cookie及oid获取方式获取你的cookie和对应视频oid")
    print("=" * 30)
    print("请按照下面提示输入需要爬取的弹幕时间，建议不要超过最近两个月")
    print("=" * 30)

    start = input("请输入弹幕开始时间，格式年-月-日，例2020-09-01：")
    end = input("请输入弹幕结束时间，格式年-月-日，例2020-09-20：")
    cookie = input("请输入你的Cookie：")
    oid = input("请输入对应视频oid：")
    name = input("请输入保存文件名称：")

    headers = HEADERS_TEMPLATE.copy()
    headers["cookie"] = "buvid3=4302AB19-E611-70CA-1961-57908865B74B50209infoc; b_nut=1721469950; _uuid=92B7CE67-694A-3E83-758C-10C44CC4B2C8E49110infoc; buvid_fp=93280bb7744e321a1276cc11e5adc33b; enable_web_push=DISABLE; buvid4=ACEA04B4-1C82-1D71-B4B1-EC634D3888AD51140-024072010-sZIurRVWX2DwMqIkjxRz8w%3D%3D; home_feed_column=5; SESSDATA=ff91df84%2C1737021999%2C7364e%2A72CjDgC3XYaUNRM8HApZbWL25U4KHA1vuWGf0wZlMPXCVsdy_vTpYNR9sHOcKb0-qYVi4SVmVNTTg3V084YTdoVlVkQjJjTkZESVVwbHRSRWtTYVRoUzVOSmdoc01JWmViZTBBdzEwUThpVnVLcHJhdmhoV19GUmsydFliY2xqNi10SlZZZkt1a2RnIIEC; bili_jct=aa635a1167266cfb774a694d19215efd; DedeUserID=440135686; DedeUserID__ckMd5=0b70536606dd68ab; header_theme_version=CLOSE; CURRENT_FNVAL=4048; rpdid=|(Yl)m|kmJk0J'u~kuR~||JJ; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjE3MjkzNTAsImlhdCI6MTcyMTQ3MDA5MCwicGx0IjotMX0.sGBCVK5dYKq4RDI5XAbox-kbPuvhPS_4TTjKxw3DH6w; bili_ticket_expires=1721729290; b_lsid=102C105D46_190D0676D7A; browser_resolution=1707-811; bp_t_offset_440135686=956252856178966528; sid=nmwkq99q"
    headers["referer"] = f"https://www.bilibili.com/video/BV19z421q7GM/?spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=5ec0bdf3923f0e72967dd9c6650e7943&oid={oid}"

    print("========正在爬取弹幕=========")
    url_list = get_danmu_urls(oid, start, end)
    danmakus = download_and_parse_danmu(url_list, headers)

    print("========正在保存弹幕文本文件========")
    save_danmu_to_file(danmakus, name)

if __name__ == "__main__":
    main()
