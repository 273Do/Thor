import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap 
    
# 時間をヒートマップの形式に対応するように変換する関数
ConvertToHeatmapCompatible = lambda time: int(288 * time / 24)

# 歩数から睡眠を推定する関数
def estimateSleepFromStep(mode, time_specified_data, step_observation_threshold, file_name):
    
    # 日を跨ぐかどうか
    is_cross_day = True
    
    # ステップ観測閾値が9~24の間であるかどうかを判断する必要があるか？
    
    if(12 < time_specified_data[0] <= 24):
        is_cross_day = False
    
    bed_time_average = ConvertToHeatmapCompatible(time_specified_data[0])
    wake_time_average = ConvertToHeatmapCompatible(time_specified_data[1])
    
    if(time_specified_data[2] == "-"):
        bed_time_threshold = ConvertToHeatmapCompatible(2)
    else:
        bed_time_threshold = ConvertToHeatmapCompatible(time_specified_data[2])
    if(time_specified_data[3] == "-"):
        wake_time_threshold = ConvertToHeatmapCompatible(2)
    else:
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
    unique_dates = df['startDate'].dt.date.unique().tolist()
    heatmap_data = np.zeros((len(unique_dates), 288))  # 288は24時間 x 60分 / 5分刻み
    
    # 推定するアルゴリズムを実装
    for i, date in enumerate(unique_dates):
        date_data = df[df['startDate'].dt.date == date]
        set_bed_time = False
        set_wake_time = False
        is_skip = False
        end_tmp = 0
        estimate_index_array = [[], []]
        
        for _, row in date_data.iterrows():
            start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
            end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
            if(start_index - end_tmp > ConvertToHeatmapCompatible(step_observation_threshold)):#9_15
                is_skip = True
                # print(row["startDate"].strftime("%Y-%m-%d"), unique_dates[i])
                # unique_dates.remove(row["startDate"].strftime("%Y-%m-%d"))
                # 日にちを消す処理をしたい
                # delete_date_index.append(unique_dates[i])
                # del unique_dates[i]
                break
            else:
                is_skip = False
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
            end_tmp = end_index
          
        # 日をスキップしない場合はヒートマップ用のデータを更新  
        if(is_skip == False):
            # 平均就寝時間が24時を超えない場合とそうでない場合
            # 各行に対して、startDate から endDate の範囲を1に設定
            if(is_cross_day == False):
                heatmap_data[i, max(estimate_index_array[0]):288] = 1
                heatmap_data[i, 0:min(estimate_index_array[1])] = 1
            else:
                heatmap_data[i, max(estimate_index_array[0]):min(estimate_index_array[1])] = 1

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