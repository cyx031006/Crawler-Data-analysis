import re

def clean_danmu_content(danmakus):
    """
    清洗弹幕内容，去除每行前面的无效内容

    :param danmakus: 弹幕内容列表
    :return: 清洗后的弹幕内容列表
    """
    cleaned_danmakus = []

    for danmu in danmakus:
        # 去除每行前面的无效内容，只保留中文字符、英文字符、数字和标点符号
        danmu = re.sub(r'^[^\u4e00-\u9fa5a-zA-Z0-9，。！？、；：‘’“”（）【】《》]*', '', danmu)
        # 去除空白行
        if danmu.strip():
            cleaned_danmakus.append(danmu.strip())

    return cleaned_danmakus

def read_danmu_file(file_path):
    """
    读取弹幕文件内容

    :param file_path: 文件路径
    :return: 弹幕内容列表
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_danmu_file(file_path, danmakus):
    """
    将弹幕内容写入文件

    :param file_path: 文件路径
    :param danmakus: 弹幕内容列表
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for danmu in danmakus:
            file.write(danmu + '\n')

def main():
    # 读取原始弹幕内容文件
    input_file_path = 'output/弹幕内容.txt'
    output_file_path = 'output/clean弹幕内容.txt'

    danmakus = read_danmu_file(input_file_path)

    print("========原始弹幕内容========")
    for danmu in danmakus[:10]:  # 打印前10条原始弹幕
        print(danmu.strip())

    # 清洗弹幕内容
    cleaned_danmakus = clean_danmu_content(danmakus)

    print("\n========清洗后的弹幕内容========")
    for danmu in cleaned_danmakus[:10]:  # 打印前10条清洗后的弹幕
        print(danmu)

    # 将清洗后的弹幕内容写入新文件
    write_danmu_file(output_file_path, cleaned_danmakus)

    print(f"\n清洗后的弹幕内容已保存到 {output_file_path}")

if __name__ == "__main__":
    main()
