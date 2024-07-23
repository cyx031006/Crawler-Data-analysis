from snownlp import SnowNLP

def read_danmu_file(file_path):
    """读取弹幕内容文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def analyze_sentiment(danmakus):
    """分析弹幕的情感"""
    sentiments = [SnowNLP(danmu).sentiments for danmu in danmakus]
    return sentiments

def main():
    input_file_path = 'output/clean弹幕内容.txt'
    danmakus = read_danmu_file(input_file_path)

    # 进行情感分析
    sentiments = analyze_sentiment(danmakus)
    average_sentiment = sum(sentiments) / len(sentiments)

    print(f"所有弹幕的平均情感分数是: {average_sentiment:.2f}")

    # 保存结果到文件（可选）
    with open('output/sentiment_analysis_results.txt', 'w', encoding='utf-8') as file:
        file.write(f"所有弹幕的平均情感分数是: {average_sentiment:.2f}\n")
        file.write("\n弹幕情感分数如下:\n")
        for idx, sentiment in enumerate(sentiments):
            file.write(f"弹幕 {idx + 1}: {sentiment:.2f}\n")

    print("情感分析结果已保存到 sentiment_analysis_results.txt")

if __name__ == "__main__":
    main()
