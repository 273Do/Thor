import pandas as pd
from module.time_function import shift_time, time_to_minutes
from datetime import datetime

# all_output_data.csvのactual_bed,actual_wakeとestimate_bed,estimate_wakeからデータ取得し，
# 時間ごとに平均の差分をとる．
# その時間ごとの最大値と最小値を取得する．


def extraction_of_errorForEachTime(interval):
    # 結果を格納するオブジェクト
    # 形式...0~2:[bed, wake],2~4:[bed, wake],4~6:[bed, wake],...

    result = {}

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

    print(df)

    # 時間ごとに処理を実行
    for i in range(0, 24, interval):

        time_range = [i, i+interval]
        if i+interval > 24:
            time_range = [i, 24]
        print(time_range)

        # time_rangeの範囲内のそれぞれのデータを取得
        bed_diff_df = df[(df['actual_bed'].dt.hour >= i) & (
            df['actual_bed'].dt.hour < i+interval)][['bed_diff_minutes']]
        wake_diff_df = df[(df['actual_wake'].dt.hour >= i) & (
            df['actual_wake'].dt.hour < i+interval)][['wake_diff_minutes']]

        print(f"就寝時間平均誤差:{bed_diff_df.mean().values[0]}")
        print(f"起床時間平均誤差:{wake_diff_df.mean().values[0]}")
        print(f"就寝時間最大誤差:{bed_diff_df.max().values[0]}")
        print(f"就寝時間最小誤差:{bed_diff_df.min().values[0]}")
        print(f"起床時間最大誤差:{wake_diff_df.max().values[0]}")
        print(f"起床時間最小誤差:{wake_diff_df.min().values[0]}")

    # 時間ごとのデータを取得
    # time_df = df[(df['date'].dt.hour >= i) & (df['date'].dt.hour < i+interval)]
    # print(time_df)


# 引数に時間間隔を指定
extraction_of_errorForEachTime(2)
# 誤差597分o12,0228のデータ
