import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap 

# 時間をヒートマップの形式に対応するように変換する関数
def ConvertToHeatmapCompatible(time):
    return int(288 * time / 24)

# 歩数から睡眠を推定する関数
def estimateSleepFromStep(mode,time_specified_data,file_name):
    
    bed_time_average = ConvertToHeatmapCompatible(time_specified_data[0])
    wake_time_average = ConvertToHeatmapCompatible(time_specified_data[1])
    bed_time_threshold = ConvertToHeatmapCompatible(time_specified_data[2])
    wake_time_threshold = ConvertToHeatmapCompatible(time_specified_data[3])
    
    # CSVファイルを読み込む
    df = pd.read_csv(mode["metadata"]["csv_file_path"], dtype={"sourceVersion": str, "device": str}, low_memory=False)
    
    # 指定の日付範囲でフィルタリング
    df = df[(df["startDate"] >= mode["metadata"]["start_date"]) & (df["endDate"] <= mode["metadata"]["end_date"])]
    
    # "startDate" と "endDate" の列を datetime 型に変換
    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    
    # 抽出対象を指定してフィルタリング
    df = df[df["device"].str.contains("name:iPhone")]
    
    # ヒートマップ用のデータを初期化
    unique_dates = df['startDate'].dt.date.unique()
    heatmap_data = np.zeros((len(unique_dates), 288))  # 288は24時間 x 60分 / 5分刻み
    
    # 各行に対して、startDate から endDate の範囲を1に設定
    # 推定するアルゴリズムを実装
    for i, date in enumerate(unique_dates):
        date_data = df[df['startDate'].dt.date == date]
        # print(date_data)
        set_bed_time = False
        set_wake_time = False
        estimate_index_array = [[],[]]
        for _, row in date_data.iterrows():
            start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
            end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
            # print(start_index,end_index)
        
            if((abs(end_index - bed_time_average) < bed_time_threshold)):
                estimate_index_array[0].append(end_index)
                set_bed_time = True
            elif(set_bed_time == False):
                estimate_index_array[0].append(bed_time_average)
            if((abs(start_index - wake_time_average) < wake_time_threshold)):
                estimate_index_array[1].append(start_index)
                set_wake_time = True
            elif(set_wake_time == False):
                estimate_index_array[1].append(wake_time_average)
        # print(estimate_index_array)
        heatmap_data[i, max(estimate_index_array[0]):min(estimate_index_array[1]) + 1] = 1
        
        # print("----day:",row['startDate'].day,"----")
        
    # ヒートマップの描画
    plt.figure()  # 新しいFigureを作成
    plt.imshow(heatmap_data, cmap=ListedColormap(['white', 'blue']), aspect='auto', interpolation='none')

    # タイトル，軸の設定
    plt.title(mode["heatmap"]["title"])
    plt.xlabel(mode["heatmap"]["x_label"])
    plt.ylabel(mode["heatmap"]["y_label"])
    plt.yticks(range(len(unique_dates)), [date.strftime('%Y-%m-%d') for date in unique_dates], fontsize=8)
    
    # x軸の目盛りを設定
    time_labels = np.arange(0, 288, 6*12)  # 6時間ごとに目盛りを表示
    plt.xticks(time_labels, [f"{h//12}:{h%12*5:02d}" for h in time_labels])
    
    # カラーバーを表示
    cbar = plt.colorbar(ticks=[0, 1])
    cbar.set_ticklabels(mode["color_bar"]["tick_labels"])
    cbar.set_label(mode["color_bar"]["label"])
    
    # グラフを保存
    plt.savefig(mode["metadata"]["image_name"] + "_" + file_name + ".png")