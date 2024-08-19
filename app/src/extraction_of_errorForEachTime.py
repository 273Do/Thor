import pandas as pd
from module.time_function import shift_time, time_to_minutes
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# 時間ごとに平均の差分を取り，その時間ごとの最大値と最小値を取得する．


def extraction_of_errorForEachTime(interval):
    # 結果を格納するオブジェクト
    # 形式...0~2:[bed, wake],2~4:[bed, wake],4~6:[bed, wake],...

    labels = []
    all_diff_mean = []
    bed_diff_mean = []
    wake_diff_mean = []
    bed_diff_max = []
    wake_diff_max = []
    bed_diff_min = []
    wake_diff_min = []

    # intervalが24以下でない場合はエラーを出力
    if interval > 24:
        print("intervalは24以下で指定してください.")
        return

    # CSVファイルを読み込む
    df = pd.read_csv("extraction_data/z_all_output/all_output_data.csv")
    # actual_bed,actual_wakeとestimate_bed,estimate_wakeを抽出
    df = df[(df['mode'] == "Median")][['date', 'actual_bed',
                                       'actual_wake', 'estimate_bed', 'estimate_wake']]

    # "startDate" と "endDate" の列を datetime 型に変換
    df['actual_bed'] = pd.to_datetime(df['actual_bed'])
    df['actual_wake'] = pd.to_datetime(df['actual_wake'])
    df['estimate_bed'] = pd.to_datetime(df['estimate_bed'])
    df['estimate_wake'] = pd.to_datetime(df['estimate_wake'])

    # データの各行に対して時間差を分に変換して格納
    df['bed_diff_minutes'] = df.apply(lambda row: time_to_minutes(
        datetime.strptime(shift_time(row['actual_bed'], row['estimate_bed'])[1], "%H:%M").strftime("%H:%M")), axis=1)
    df['wake_diff_minutes'] = df.apply(lambda row: time_to_minutes(
        datetime.strptime(shift_time(row['actual_wake'], row['estimate_wake'])[1], "%H:%M").strftime("%H:%M")), axis=1)

    all_diff_mean.append(round(df['bed_diff_minutes'].mean(), 2))
    all_diff_mean.append(round(df['wake_diff_minutes'].mean(), 2))

    print("全体の平均誤差:", all_diff_mean)

    # 時間ごとに処理を実行
    for i in range(0, 24, interval):

        time_range = [i, i+interval]
        if i+interval > 24:
            time_range = [i, 24]

        # time_rangeの範囲内のそれぞれのデータを取得
        bed_diff_df = df[(df['actual_bed'].dt.hour >= time_range[0]) & (
            df['actual_bed'].dt.hour < time_range[1])][['bed_diff_minutes']]
        wake_diff_df = df[(df['actual_wake'].dt.hour >= time_range[0]) & (
            df['actual_wake'].dt.hour < time_range[1])][['wake_diff_minutes']]

        # ラベルを格納
        # labels.append(
        #     f"{time_range[0]}~{time_range[1]}\nMax:{bed_diff_df.max().values[0]}\nMin:{bed_diff_df.min().values[0]}")
        labels.append(
            f"{time_range[0]}~{time_range[1]}")

        # 結果を格納
        bed_diff_mean.append(round(bed_diff_df.mean().values[0], 2))
        wake_diff_mean.append(round(wake_diff_df.mean().values[0], 2))
        bed_diff_max.append(
            round(bed_diff_df.max().values[0], 2))
        wake_diff_max.append(
            round(wake_diff_df.max().values[0], 2))
        bed_diff_min.append(round(bed_diff_df.min().values[0], 2))
        wake_diff_min.append(round(wake_diff_df.min().values[0], 2))

    print("就寝時間平均誤差:", bed_diff_mean)
    print("起床時間平均誤差:", wake_diff_mean)
    print("就寝時間最大誤差:", bed_diff_max)
    print("起床時間最大誤差:", wake_diff_max)
    print("就寝時間最小誤差:", bed_diff_min)
    print("起床時間最小誤差:", wake_diff_min)

    graph_of_errorForEachTime(interval, labels, all_diff_mean,
                              bed_diff_mean, wake_diff_mean, bed_diff_max, wake_diff_max, bed_diff_min, wake_diff_min)

    # print(f"就寝時間平均誤差:{bed_diff_df.mean().values[0]}")
    # print(f"起床時間平均誤差:{wake_diff_df.mean().values[0]}")
    # print(f"就寝時間最大誤差:{bed_diff_df.max().values[0]}")
    # print(f"就寝時間最小誤差:{bed_diff_df.min().values[0]}")
    # print(f"起床時間最大誤差:{wake_diff_df.max().values[0]}")
    # print(f"起床時間最小誤差:{wake_diff_df.min().values[0]}")

    # 時間ごとのデータを取得
    # time_df = df[(df['date'].dt.hour >= i) & (df['date'].dt.hour < i+interval)]
    # print(time_df)


# 結果のグラフ化


def graph_of_errorForEachTime(interval, labels, all_diff_mean, bed_diff_mean, wake_diff_mean, bed_diff_max, wake_diff_max, bed_diff_min, wake_diff_min):

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, bed_diff_mean, width,
                    label='bed', color='#08306b')
    rects2 = ax.bar(x + width/2, wake_diff_mean, width,
                    label='wake', color='#aacfe5')

    ax.set_ylabel('Mean Error Time(s)')
    ax.set_xlabel('Time(h)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, size=8)
    ax.legend()

    plt.text(-0.5, 500,
             f"All Diff Mean\nbed:{all_diff_mean[0]}s\nwake:{all_diff_mean[1]}s", fontsize=10)

    def autolabel(rects):
        for i, rect in enumerate(rects):
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', size=8)

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()
    plt.savefig(
        f"extraction_data/z_all_output/extraction_of_errorForEachTime_{interval}h.png")


# 引数に時間間隔を指定
extraction_of_errorForEachTime(6)
# 誤差597分o12,0228のデータ
