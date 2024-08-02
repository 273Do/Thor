import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.colors import ListedColormap

# 引数は以下の通りで，オブジェクトしてまとめる
# mode, metadata，heatmap，colorbar
# metadata:csv_file_path, start_date, end_date, device_name, image_name, heatmap_config
# heatmap:title．x_label, y_label
# colorbar:ticklabels(二次元)，label

# device_name
# mode

# データ可視化用の関数


def phone_data_visualization(mode, subject_data):

    # 時間の設定を読み込む
    json_open = open('./src/settings.json', 'r')
    time = json.load(json_open)

   # CSVファイルを読み込む
    df = pd.read_csv(mode["metadata"]["csv_file_path"].replace(
        "{ID_HERE}", f"{subject_data[0]}_{subject_data[1]}_{subject_data[2]}"), low_memory=False)

   # 指定の日付範囲でフィルタリング
    df = df[(df["startDate"] >= time["time"]["start_date"])
            & (df["endDate"] <= time["time"]["end_date"])]

    # 抽出対象を指定してフィルタリング
    if (mode["mode_name"] == "sleep"):
        # デバイス名を取得
        df = df[(df["sourceVersion"].str.contains("17")) & (
                df["value"] == "HKCategoryValueSleepAnalysisInBed")]
    elif (mode["mode_name"] == "step"):
        df = df[df["device"].str.contains("name:iPhone")]

    # "startDate" と "endDate" の列を datetime 型に変換
    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])

    # ヒートマップ用のデータを初期化
    unique_dates = pd.date_range(start=time["time"]["start_date"], end=datetime.strptime(
        time["time"]["end_date"], "%Y-%m-%d") - timedelta(days=1)).date
    heatmap_data = np.zeros((len(unique_dates), 288))  # 288：24時間 x 60分 / 5分刻み

    # 各行に対して、startDate から endDate の範囲を1に設定
    for i, date in enumerate(unique_dates):
        date_data = df[df['startDate'].dt.date == date]
        for _, row in date_data.iterrows():
            start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour *
                              60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
            end_index = int(
                (row['endDate'].hour * 60 + row['endDate'].minute) / 5)
            heatmap_data[i, start_index:end_index + 1] = 1

    # ヒートマップの描画
    plt.figure()  # 新しいFigureを作成
    plt.imshow(heatmap_data, cmap=ListedColormap(
        ['#ffffff', '#08306b']), aspect='auto', interpolation='none')

    # タイトル，軸の設定
    plt.title(mode["heatmap"]["title"])
    plt.xlabel(mode["heatmap"]["x_label"])
    plt.ylabel(mode["heatmap"]["y_label"])
    plt.yticks(range(len(unique_dates)), [date.strftime(
        '%Y-%m-%d') for date in unique_dates], fontsize=8)

    # x軸の目盛りを設定
    time_labels = np.arange(0, 288, 6*12)  # 6時間ごとに目盛りを表示
    plt.xticks(time_labels, [f"{h//12}:{h%12*5:02d}" for h in time_labels])

    # カラーバーを表示
    cbar = plt.colorbar(ticks=[0, 1])
    cbar.set_ticklabels(mode["color_bar"]["tick_labels"])
    cbar.set_label(mode["color_bar"]["label"])

    # グラフを保存
    plt.savefig(mode["metadata"]["image_name"] + subject_data[0] + "_sp.png")
