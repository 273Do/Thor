import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap

# データ可視化用の関数
def dataVisualization(mode, file_name):

    # 時間の設定を読み込む
    json_open = open('./src/settings.json', 'r')
    time = json.load(json_open)
    
    # CSVファイルを読み込む
    df = pd.read_csv(mode["metadata"]["csv_file_path"], low_memory=False)
    
    # 指定の日付範囲でフィルタリング
    df = df[(df["startDate"] >= time["time"]["start_date"]) & (df["endDate"] <= time["time"]["end_date"])]
    
    # "startDate" と "endDate" の列を datetime 型に変換
    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    
    # 抽出対象を指定してフィルタリング
    if(mode["mode_name"] == "sleep"):
        # デバイス名を取得
        device_name = df["sourceName"].mode()[0]
        print("sleepデバイス名：" + device_name)
        df = df[(df["sourceName"] == device_name) & (df["value"] == "HKCategoryValueSleepAnalysisInBed")]
    elif(mode["mode_name"]  == "step"):
        df = df[df["device"].str.contains("name:iPhone")]
    
    # ヒートマップ用のデータを初期化
    unique_dates = df['startDate'].dt.date.unique()
    heatmap_data = np.zeros((len(unique_dates), 288))  # 288：24時間 x 60分 / 5分刻み
    
    # 各行に対して、startDate から endDate の範囲を1に設定
    for i, date in enumerate(unique_dates):
        date_data = df[df['startDate'].dt.date == date]
        for _, row in date_data.iterrows():
            start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
            end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
            heatmap_data[i, start_index:end_index + 1] = 1
            
    # ヒートマップの描画
    plt.figure()  # 新しいFigureを作成
    plt.imshow(heatmap_data, cmap=ListedColormap(['white', 'blue']), aspect='auto', interpolation='none')

    # タイトル，軸の設定
    plt.title(mode["heatmap"]["title"])
    plt.xlabel(mode["heatmap"]["x_label"])
    plt.ylabel(mode["heatmap"]["y_label"])
    plt.yticks(range(len(unique_dates)), [date.strftime('%Y-%m-%d') for date in unique_dates], fontsize=8)
    
    # x軸の目盛りを設定
    time_labels = np.arange(0, 289, 6*12)  # 6時間ごとに目盛りを表示
    plt.xticks(time_labels, [f"{h//12}:{h%12*5:02d}" for h in time_labels])
    
    # カラーバーを表示
    cbar = plt.colorbar(ticks=[0, 1])
    cbar.set_ticklabels(mode["color_bar"]["tick_labels"])
    cbar.set_label(mode["color_bar"]["label"])
    
    # グラフを保存
    plt.savefig(mode["metadata"]["image_name"] + "_" + file_name + ".png")