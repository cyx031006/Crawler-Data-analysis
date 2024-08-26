from pyecharts import options as opts
from pyecharts.charts import Bar
from snownlp import SnowNLP


def read_danmu_file(file_path):
    """读取弹幕内容文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def analyze_sentiment(danmakus):
    """分析弹幕的情感"""
    sentiments = [SnowNLP(danmu).sentiments for danmu in danmakus]
    return sentiments


def generate_sentiment_distribution_chart(sentiments):
    """生成情感分布图"""
    sentiment_bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
    sentiment_labels = ['非常负面', '负面', '中性', '正面', '非常正面']

    # 计算每个区间的频次
    sentiment_counts = [0] * (len(sentiment_bins) - 1)
    for sentiment in sentiments:
        for i in range(len(sentiment_bins) - 1):
            if sentiment_bins[i] <= sentiment < sentiment_bins[i + 1]:
                sentiment_counts[i] += 1
                break

    bar = Bar()
    bar.add_xaxis(sentiment_labels)
    bar.add_yaxis('情感分布', sentiment_counts)
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="弹幕情感分布图"),
        xaxis_opts=opts.AxisOpts(name="情感倾向"),
        yaxis_opts=opts.AxisOpts(name="弹幕数量")
    )

    return bar


def create_danmu_html():
    input_file_path = 'output/clean弹幕内容.txt'
    sentiment_chart_path = 'output/sentiment_distribution.html'
    keyword_trend_chart_path = 'keyword_trend.html'

    # 读取弹幕内容
    danmakus = read_danmu_file(input_file_path)

    # 情感分析
    sentiments = analyze_sentiment(danmakus)

    # 生成情感分布图
    sentiment_chart = generate_sentiment_distribution_chart(sentiments)
    sentiment_chart.render(sentiment_chart_path)



if __name__ == "__main__":
    create_danmu_html()
