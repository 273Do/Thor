import pandas as pd
import numpy as np
import calendar
import math
import json
from datetime import datetime
# from src.module.time_function import median_time, shift_time, time_to_minutes
from time_function import median_time, shift_time, time_to_minutes

# 記録月を格納した配列
month_list = [12, 1, 2]

# 個人の平均を格納する配列
individual_ave = {
    # 't07': {12: [], 1: [], 2: []}
}


# 個人の平均を取得する関数

def get_individual_average(question_per_month, months):

    # all_output_data.csvのestimate_bed,estimate_wakeからデータ取得

    # データの読み込み
    df = pd.read_csv("extraction_data/z_all_output/all_output_data_n.csv")

    # idのリストを作成
    id_list = df["id"].unique()

    # 日付列をdatetime型に変換
    df['date'] = pd.to_datetime(df['date'])

    # 使用できるデータを抽出
    available_diff_bed_data_df = df[(df['mode'] == "Median")]

    # idごとに補正値を算出
    for id in id_list:

        # IDごとの辞書を初期化
        individual_ave[id] = {month: [] for month in months}

        # idごとのデータを取得
        id_df = available_diff_bed_data_df[available_diff_bed_data_df["id"] == id]
        print(f"{id}-----------------")

        # filtered_dfs = []
        # 月ごとのデータを取得
        for month in months:
            # 正解データ数
            data_count = id_df[id_df['date'].dt.month == month].shape[0]

            # その月の日数
            days = calendar.monthrange(2024, month)[1]

            # 分割数(正解データに対するその月の質問回数)
            # split = round(data_count * question_per_month / days)
            # split = (data_count * question_per_month / days)

            split = math.ceil(data_count * question_per_month / days)
            if ((split == 0) & (data_count > 0)):
                split = 1

            # 参照するデータの間隔(n日ごとに)
            split_cnt = math.floor(days/question_per_month)

            # 参照するデータの日にち
            monthly_df = id_df[id_df['date'].dt.month == month]
            # filtered_dfs.append(monthly_df["date"].iloc[0::split_cnt])

            print(f"{month}-count:{data_count}")
            print(f"{month}-days:{days}")
            print(f"{month}-split:{split}回質問")

            # 差分をとる日のdf
            diff_df = monthly_df.iloc[0::split_cnt]
            # splitが1でデータ数が2以上の時最後のデータを削除
            # print(monthly_df["date"].iloc[0::split_cnt])
            # if ((split > 0) & (diff_df.shape[0] > 1)):
            # diff_df = diff_df[:-1]

            # print(diff_df[['date', 'actual_bed', 'actual_wake',
            #       'estimate_bed', 'estimate_wake']])
            # print(diff_df["date"])

            # 就寝と起床の実際と推定の差を取得
            available_diff_bed_data = diff_df.apply(lambda row: time_to_minutes(
                datetime.strptime(shift_time(row['estimate_bed'], row['actual_bed'])[1], "%H:%M").strftime("%H:%M")), axis=1)
            available_diff_wake_data = diff_df.apply(lambda row: time_to_minutes(
                datetime.strptime(shift_time(row['estimate_wake'], row['actual_wake'])[1], "%H:%M").strftime("%H:%M")), axis=1)
            # print(f"就寝：{available_diff_bed_data}, 起床：{available_diff_wake_data}")

            # 差の平均を求める
            average_diff_bed = format(np.mean(
                available_diff_bed_data), ".0f")
            average_diff_wake = format(np.mean(
                available_diff_wake_data), ".0f")
            print(f"就寝：{average_diff_bed}, 起床：{average_diff_wake}")

            # その月にデータがない場合はNoneに変換
            if (average_diff_bed == "nan"):
                average_diff_bed = '0'
            if (average_diff_wake == "nan"):
                average_diff_wake = '0'

            # 辞書に格納
            individual_ave[id][month] = [
                average_diff_bed, average_diff_wake]

    # print(individual_ave)
    # JSONファイルに保存
    with open("extraction_data/z_all_output/individual_ave.json", "w") as f:
        json.dump(individual_ave, f, ensure_ascii=False, indent=1)

    # 検証条件を出力
    print("-------検証条件-------")
    print(f'1ヶ月あたりの質問回数：{question_per_month}回')
    print("日数")
    for month in months:
        print(f"{month}月：{calendar.monthrange(2024, month)[1]}日")
        print(
            f"次の質問の日間隔：{math.floor(calendar.monthrange(2024, month)[1]/question_per_month)}日")


# 30日ある月に対し，3分割するとして，17個データがある場合，
# 30/3=10日をカウントし始めるごとに質問する．よって，２回質問する．
get_individual_average(3, month_list)
